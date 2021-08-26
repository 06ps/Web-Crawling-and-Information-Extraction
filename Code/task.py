""" 
    Name : Pratibha Singh (pratibhasingh@kgpian.iitkgp.ac.in)
    Roll No : 20CS60R12

    File name : task1.py
    Date : April 1, 2021
"""

# importing required modules
import sys
import urllib.request
import re
import itertools
import unicodedata
import ply.lex as lex
import ply.yacc as yacc
import re

# Function to convert latin letters to English alphabet 
def latin_to_aplha(text):
    return ''.join(char for char in unicodedata.normalize('NFKD', text)
    if unicodedata.category(char) != 'Mn')

# creating dictionary class
class my_dictionary(dict):

    def __init__(self):
        self = dict()

    # function to add key value pair
    def add(self, key, value):
        self[key] = value
    
    
# creating a dictionary
result = my_dictionary()
field_list = ['Movie_Name', 'Director', 'Writer', 'Producer', 'Original Language', 'Cast with the Character name', 'Storyline', 'Box office collection', 'Runtime', 'You might also like', 'Where to watch']

#list to store all cast and crew names, director name, might like list and where to watch
cast_char_name = []
dir_name = []
might_like = []
watch = []
might_like_url = []
cast_url = []

# creating a dictionary to store cast results
cast_result = my_dictionary()
cast_field = ['Highest Rated film', 'Lowest Rated film', 'Birthday']

# initialzing all key value of dictonary as ''(empty string)
for i in field_list:
    result.add(i, '')

for i in cast_field:
    cast_result.add(i, '')

# creating dictonary to store all movie list with year of a particular cast
movie_list_year = {}


# token list used
tokens = [
    'MOVIE_S', 'MOVIE_E',
    'DIRECTOR', 'DIR_CLOSE',
    'WHITE_SPACE',
    'NAME',
    'WRITER', 'CLOSE',
    'ESTART',
    'PRODUCER',
    'LANG',
    'STORY',
    'BOXOFFICE',
    'RUNTIME', 'REND',
    'RNAME', 'CEND', 'MID',
    'LIKE_S',
    'WATCH_S', 'WATCH_E',
    'LINK_S', 'LINK_E',
    'CAST_E',
    'BIRTH_S', 'BIRTH_E',
    'HIGH', 'LOW', 'HL_END',
    'MOVIE_LIST','MOVIE_YEAR', 'MY_C',
    'W_LINK_S'
]

# Regular expression for each tokens
def t_MOVIE_S(t):
    r'<meta\sproperty=\"og:title\"\scontent=\"'
    return t

def t_MOVIE_E(t):
    r'\">'
    return t

def t_DIRECTOR(t):
    r'<a\shref=\"[a-zA-Z0-9\/_\-:]+\"\sdata-qa=\"movie-info-director\">'
    return t

def t_ESTART(t):
    r'\s*<a\shref=\"[\/a-zA-Z_0-9\-:]+\">'
    return t

def t_DIR_CLOSE(t):
    r'<\/a>\s*,*'
    return t

def t_WRITER(t):
    r'Writer:<\/div>\s*.*\">\s*'
    return t

def t_PRODUCER(t):
    r'Producer:<\/div>\s*.*\">\s*'
    return t

def t_LANG(t):
    r'Original\sLanguage:<\/div>\s*.*\">'
    return t

def t_STORY(t):
    r'data-qa=\"movie-info-synopsis\">\s*'
    return t

def t_BOXOFFICE(t):
    r'Box\sOffice\s\(Gross\sUSA\):<\/div>\s*.*\">'
    return t

def t_RUNTIME(t):
    r'<time\sdatetime=\"P.*M\">\s*'
    return t

def t_REND(t):
    r'\s*<\/time>'
    return t

def t_RNAME(t):
    r'span\stitle=\"[\u00C0-\u00CF\u00D0-\u00DF\u00E0-\u00EF\u00F0-\u00FFa-zA-z0-9\s\-_&#;\'.]+\">\s*'
    return t

def t_MID(t):
    r'\s*<\/span>\s*.*\s*<span\sclass=\"characters\ssubtle\ssmaller\"\stitle=\"[\u00C0-\u00CF\u00D0-\u00DF\u00E0-\u00EF\u00F0-\u00FFa-zA-Z0-9&#;\s\-_&\'.]+\">\s*<br\/>\s*'
    return t

def t_LIKE_S(t):
    r'class=\"recommendations-panel__poster-title\">'
    return t

def t_WATCH_S(t):
    r'<affiliate-icon\sname=\"'
    return t

def t_WATCH_E(t):
    r'\"\salignicon'
    return t

def t_LINK_S(t):
    r'<a\shref=\"\s*'
    return t

def t_LINK_E(t):
    r'\"\sclass=\"recommendations-panel__poster-link\">'
    return t

def t_CAST_E(t):
    r'\s*\"\sclass=\"unstyled\sarticleLink\"\sdata-qa=\"cast-crew-item-link\">\s*'
    return t

def t_W_LINK_S(t):
    r'<div\sclass=\"media-body\">\s*'
    return t

def t_BIRTH_S(t):
    r'data-qa=\"celebrity-bio-bday\">\s*Birthday:\s*'
    return t

def t_BIRTH_E(t):
    r'\s*<\/p>'
    return t

def t_HIGH(t):
    r'Highest\sRated:\s*<span\sclass=\"label\">\s*.*\s*.*\s*.*\s*.*\s*<a\sclass="celebrity-bio__link\".*\s*'
    return t

def t_LOW(t):
    r'Lowest\sRated:\s*<span\sclass=\"label\">\s*.*\s*.*\s*.*\s*.*\s*<a\sclass="celebrity-bio__link\".*\s*'
    return t

def t_HL_END(t):
    r'\s*<\/a>'
    return t

def t_MOVIE_LIST(t):
    r'<tr\s*data-title=\"'
    return t

def t_MOVIE_YEAR(t):
    r'\"\s*data-boxoffice=\".*\"\s*data-year=\"'
    return t

def t_MY_C(t):
    r'\"'
    return t

def t_CEND(t):
    r'\s*<(br\/|\/span)>'
    return t

def t_CLOSE(t):
    r'\s*<\/div>'
    return t

def t_NAME(t):
    #r'[a-zA-Z]+'
    r'[\u00C0-\u00CF\u00D0-\u00DF\u00E0-\u00EF\u00F0-\u00FFa-zA-z0-9,.\(\)$\-&!?:_\';#\/]+'
    return t


t_WHITE_SPACE = r'[\ \t]+'

def t_error(t):
    #print("Illegal Characters")
    t.lexer.skip(1)

# Parser Rules
def p_start(var):
    '''
    start : movie_name
          | dir_name
          | writer_name
          | producer_name
          | language
          | cast
          | cast_only_name
          | cast_wl
          | cast_only_name_wl
          | storyline
          | boxoffice
          | runtime
          | might_like
          | watch
          | might_like_link
          | birthday
          | Highest_Rated
          | Lowest_Rated
          | movie_list
    '''

# Extracting movie name
def p_movie_name(var):
    'movie_name : MOVIE_S name MOVIE_E'
    result.add('Movie_Name', var[2])

# Extracting director names
def p_dir_name(var):
    'dir_name : DIRECTOR name DIR_CLOSE'
    res = var[2]
    dir_name.insert(len(dir_name), res)

# Extracting Writer names
def p_writer_name(var):
    'writer_name : WRITER expression CLOSE'
    result.add('Writer', var[2])

# Extracting producer names
def p_producer_name(var):
    'producer_name : PRODUCER expression CLOSE'
    result.add('Producer', var[2])

# Extracting language
def p_language(var):
    'language : LANG name CLOSE'
    result.add('Original Language', var[2])

# Extracting Cast and Crew names and urls
def p_cast(var):
    'cast : W_LINK_S LINK_S name CAST_E RNAME name MID name CEND'
    res = var[6] + ' as ' + var[8]
    cast_char_name.insert(len(cast_char_name), res)
    cast_url.insert(len(cast_url), var[3])

def p_cast_wl(var):
    'cast_wl : W_LINK_S RNAME name MID name CEND'
    res = var[3] + ' as ' + var[5]
    cast_char_name.insert(len(cast_char_name), res)
    cast_url.insert(len(cast_url), '?')

def p_cast_only_name(var):
    'cast_only_name : W_LINK_S LINK_S name CAST_E RNAME name MID CEND'
    res = var[6] 
    cast_char_name.insert(len(cast_char_name), res)
    cast_url.insert(len(cast_url), var[3])

def p_cast_only_name_wl(var):
    'cast_only_name_wl : W_LINK_S RNAME name MID CEND'
    res = var[3] 
    cast_char_name.insert(len(cast_char_name), res)
    cast_url.insert(len(cast_url), '?')

# Extracting storyline
def p_storyline(var):
    'storyline : STORY name CLOSE'
    result.add('Storyline', var[2])

# Extracting boxoffice 
def p_boxoffice(var):
    'boxoffice : BOXOFFICE name CLOSE'
    result.add('Box office collection', var[2])

# Extracting runtime
def p_runtime(var):
    'runtime : RUNTIME name REND'
    result.add('Runtime', var[2])

# Extracting you might also like
def p_might_like(var):
    'might_like : LIKE_S name CEND'
    res = var[2]
    might_like.insert(len(might_like), res)
 
def p_might_like_link(var):
    'might_like_link : LINK_S name LINK_E'
    res = var[2]
    might_like_url.insert(len(might_like_url), res)

# Extracting where to watch
def p_watch(var):
    'watch : WATCH_S name WATCH_E'
    res = var[2]
    watch.insert(len(watch), res)  

# Extracting birthday of crew member
def p_birthday(var):
    'birthday : BIRTH_S name BIRTH_E'
    cast_result.add('Birthday', var[2])

# Extracting High rated movie of crew member
def p_Highest_Rated(var):
    'Highest_Rated : HIGH name HL_END'
    cast_result.add('Highest Rated film', var[2])

# Extracting Low rated movie of crew member
def p_Lowest_Rated(var):
    'Lowest_Rated : LOW name HL_END'
    cast_result.add('Lowest Rated film', var[2])

# Extracting the all the movie list of crew member
def p_movie_list(var):
    'movie_list : MOVIE_LIST name MOVIE_YEAR name MY_C'
    movie_list_year[var[2]] = var[4]

# Recurssive way of extraction
def p_expression_multi(var):
    'expression : expression expression'
    var[0] = var[1] + ',' + var[2]

def p_expression_single(var):
    'expression : expression'
    var[0] = var[1]

def p_expression(var):
    'expression : ESTART name DIR_CLOSE'
    var[0] = var[2]

# Extracting names using recurssive method
def p_name_one(var):
    'name : NAME'
    var[0] = var[1]

def p_name_mid(var):
    'name : NAME name'
    var[0] = var[1] + ' ' + var[2]

def p_name_multi(var):
    'name : NAME wspaces name'
    var[0] = var[1] + var[2] + var[3]

def p_wspaces(var):
    '''
    wspaces : WHITE_SPACE
            | WHITE_SPACE wspaces
    '''
    var[0] = ' '



def p_error(var):
    pass


def recurse_movie(filename):
    # building lexer and parser
    lexer = lex.lex()
    parser = yacc.yacc()

    result.add('Director', dir_name )
    result.add('Cast with the Character name', cast_char_name)
    result.add('You might also like', might_like)
    result.add('Where to watch', watch)

    # opening the html file of movie from task1
    f = open(filename)
    txt = f.read()
    txt = txt.replace('&#39;', '\'')     
    txt = txt.replace('&amp;', '&')
    txt = txt.replace('&quot;', '\"')
    txt = txt.replace('&apos;', '\'')

    lex.input(txt)

    #for tok in iter(lex.token, None):
    #    print(repr(tok.type), repr(tok.value))

    parser.parse(txt)

    while(True):
        print('\n\t\tExtract Following Fields:')
        print('1. Movie Name')
        print('2. Director')
        print('3. Writers')
        print('4. Producer')
        print('5. Original Language')
        print('6. Cast with the character name')
        print('7. Storyline')
        print('8. Box Office Collection')
        print('9. Runtime')
        print('10. You might also like')
        print('11. Where to watch')
        val = input('\nEnter Any one of the fields(Enter digit) or press \'E\' to exit:   ')

        if val == '1' or val == '3' or val == '4' or val == '5' or val == '8' or val == '9':
            user_ip = int(val)
            idx = field_list[user_ip-1]
            print('\n', idx, ':')
            if(bool(result[idx])):
                val_list = result[idx].split(',')
                for i in val_list:
                    print(i)
            else:
                print('Data Unavailable for this field')

        elif val == '7':
            user_ip = int(val)
            idx = field_list[user_ip-1]
            print('\n', idx, ':')
            if(bool(result[idx])):
                print(result[idx])
            else:
                print('Data Unavailable for this field')

        elif val == '2' or val == '11':
            user_ip = int(val)
            idx = field_list[user_ip-1]
            print('\n', idx, ':')
            if(bool(result[idx])):
                for i in result[idx]:
                    print(i)
            else:
                print('Data Unavailable for this field')

        elif val == '6':                # for cast and crew member list and then crawling the page of corresponding cast
            user_ip = int(val)
            idx = field_list[user_ip-1]
            print('\n', idx, ':')
            k = 1
            if(bool(result[idx])):
                for i in result[idx]:
                    print('{}. {}'.format(k, i))
                    k = k + 1

                #for i in range(len(cast_url)):
                #    print(cast_url[i])
                movie_name_original = result['Movie_Name']
                cast_info = input('\n Enter corresponding Cast Member number or press \'E\' to Exit:    ')

                if(cast_info == 'E'):
                    print('closing...... ')

                try:
                    if(int(cast_info) > 0 and int(cast_info) < k):
                        num = int(cast_info)                # downloading html file of  crew member
                        url = 'https://www.rottentomatoes.com'
                        if cast_url[num-1] == '?':
                            print('No URL exist for this cast member.....')
                        else:
                            url = url + cast_url[num-1]
                            print('\n')
                            print('Crawling started.......')
                            response = urllib.request.urlopen(url)
                            content = response.read()

                            cast_filename = cast_char_name[num-1] + '.html'
                            f = open(cast_filename , 'wb')
                            f.write(content)
                            f.close()
                            print('Crawling Completed.... Successfully downloaded HTML file \n')
                            file_cast = open(cast_filename)
                            cast_txt = file_cast.read()

                            cast_txt = cast_txt.replace('&#39;', '\'')
                            cast_txt = cast_txt.replace('&amp;', '&')
                            cast_txt = cast_txt.replace('&quot;', '\"')
                            cast_txt = cast_txt.replace('&apos;', '\'')

                            lex.input(cast_txt)
                            parser.parse(cast_txt)

                            while(True):
                                print('\n\t\tExtract Following Fileds:')
                                print('1. Highest Rated film')
                                print('2. Lowest Rated film')
                                print('3. Birthday')
                                print('4. His/Her other Movies')
                                ch = input('\nEnter Any one of the fields(Enter digit) or press \'B\' to go back:  ')

                                if ch == '1' or ch == '2' or ch == '3':
                                    #print(cast_result)
                                    ch_int = int(ch)
                                    idx_c = cast_field[ch_int-1]
                                    print('\n', idx_c, ':')
                                    if(bool(cast_result[idx_c])):
                                        print(cast_result[idx_c])
                                    else:
                                        print('Data Unavaialble for this field')

                                elif ch == '4':
                                    flag = 0
                                    try:                    # if enetered value by user is interger only
                                        year = int(input('\nEnter year (YYYY) format: '))
                                        print('\n\t\tMovie with year:')
                                        for i in movie_list_year:
                                            if int(movie_list_year[i]) >= int(year):
                                                print(i, '(', movie_list_year[i], ')')
                                                flag = 1

                                        if flag == 0:
                                            print('No movie exist on and after ',year)
                                    except ValueError:
                                        print("Wrong input format !!")                                

                                elif ch == 'B':
                                    print("Closing.....")
                                    break
                                
                                else:
                                    print('Enter a valid digit or \'B\'')

                    
                            movie_list_year.clear()
                    else:
                        print('Entered invalid number !!')
                
                except ValueError:
                    print('Enterted Wrong number !!')

                result['Movie_Name'] = movie_name_original

            else:
                print('Data Unavailable for this field')

        elif val == '10':                   # recursive call for movie might like
            user_ip = int(val)
            idx = field_list[user_ip-1]
            print('\n', idx, ':')
            k = 1
            if(bool(result[idx])):
                for i in result[idx]:
                    print('{}. {}'.format(k, i))
                    k = k + 1
                
                #for i in range(len(might_like_url)):
                #    print(might_like_url[i])
                
                movie_to_watch = input('\n Enter corresponding Movie you might also like number(digit) or press \'E\' to Exit:    ')
                if(movie_to_watch == 'E'):
                    print('closing......')
                    exit()
                try:
                    if(int(movie_to_watch) > 0 and int(movie_to_watch) < k):   
                        num = int(movie_to_watch)
                        url = 'https://www.rottentomatoes.com'
                        url = url + might_like_url[num-1]
                        print('\n')
                        print(might_like[num-1], 'Crawling started......')
                        response = urllib.request.urlopen(url)
                        content = response.read()

                        filename = might_like[num-1] + '.html'
                        f = open(filename , 'wb')
                        f.write(content)
                        f.close
                        print(might_like[num-1], 'Crawling Completed.... Successfully downloaded HTML file \n')
                        # clearing all list
                        cast_char_name.clear()
                        dir_name.clear()
                        might_like.clear()
                        watch.clear()
                        cast_url.clear()
                        might_like_url.clear()
                        for i in field_list:
                            result.add(i, '')
                        recurse_movie(filename)
                    else:
                        print('Entered invalid digit')
                except ValueError:
                    print('Wrong input format !!')

            else:
                print('Data Unavailable for this field')
            
        elif val == 'E':
            print("Closing......")
            exit()

        else:
            print('Incorrect format... choose a valid number')

    # closing all the files
    f.close


genre_list = ['Action &Adventure', 'Animation', 'Drama', 'Comedy', 'Mystery & Suspense', 'Horror', 'Sci-Fi', 'Documentary', 'Romance', 'Classics']
movie_list = []         # to save all top 100 movies 

genre_html = {}         # to save all genre's html files
index = 0

url_list = ['action__adventure_movies', 'animation_movies', 'drama_movies', 'comedy_movies', 'mystery__suspense_movies', 'horror_movies', 'science_fiction__fantasy_movies', 'documentary_movies', 'romance_movies', 'classics_movies']

# saving all genres html files in dictionary
print('\nCrawling Started....')
for genre in url_list:
    url = 'https://www.rottentomatoes.com/top/bestofrt/top_100_'
    url = url + genre
    url = url + '/'

    response = urllib.request.urlopen(url)
    content = response.read().decode()

    genre_html[genre_list[index]] = content
    index = index + 1
print('Crawing Completed.... susscesfully downloaded genres HTML files\n')

print('\t\tGenres List:')
print('1. Action &Adventure')
print('2. Animation')
print('3. Drama')
print('4. Comedy')
print('5. Mystery & Suspense')
print('6. Horror')
print('7. Sci-Fi')
print('8. Documentary')
print('9. Romance')
print('10. Classics')
val = input('\nEnter Any one of the genre number(Enter digit):   ')

x = 1
html = None
text = None
indx = None

# taking genre from user 
while(x):
    try:
        user_input = int(val)
        if user_input >= 1 and user_input <= 10:
            indx = genre_list[user_input-1]
            text = genre_html[indx]
            x = 0
        else:
            val = input('\nEnter number between 1-10 only:  ')
    except ValueError:
        val = input('\nEntered in wrong format!!!  Enter numeric value only:  ')
    
# converting html file in english 
html = latin_to_aplha(text)
html = html.replace('&#39;', '\'')
html = html.replace('&amp;', '&')
html = html.replace('&quot;', '\"')
html = html.replace('&apos;', '\'')

# Regular expression to find movie 
regex = "<a href=\"\/m\/[a-zA-Z0-9_-]+\"\sclass=\"unstyled\sarticleLink\">\\n\s*([a-zA-z0-9\s().,\'-:?!&]+)<\/a>"

# finding all movies name in html file using Regular expression
movies_list = re.findall(regex, html)       

# printing the names to top 100 movies for user provided genre
print('\n')
print('\t\tList of 100 top movies\n')
i = 1
for movie in movies_list:
    movie_list.append(movie)
    print('{}. {}'.format(i,movie))
    i = i+1


movie_num = input('\nEnter corresponding Movie Number(1-100):   ')

y= 1
movie_name = None

# Taking movie name as input from  the user
while(y):
    try:
        num = int(movie_num)
        if num >= 1 and num <= 100:
            movie_name = movie_list[num-1]
            y = 0
        else:
            movie_num = input('\nEnter number between 1-10 only:  ')
    except ValueError:
        movie_num = input('\nEntered in wrong format!!!  Enter numeric value only:  ')

#print(movie_name)

movie_substr = ''
for i in range(0, len(movie_name)):
    if(movie_name[i] == '('):
        break
    else:
        movie_substr = movie_substr + movie_name[i]

#print('movie_substr', movie_substr)

# Regular expression to extract movie link
movie_regex = f"<a href=\"(\/m\/[a-zA-Z0-9_\-]+)\" class=\"unstyled articleLink\">\\n\s*{movie_substr}.*?<\/a>"


# downloading user prvided movie name of a particular genre HTML file
output = re.findall(movie_regex, html)

url = 'https://www.rottentomatoes.com'
url = url + output[0]
#url = url + '/'
#print('output',output[0],url)

print('\n')
print(movie_name, ' Crawling Started.....')
response = urllib.request.urlopen(url)
content = response.read()

file_name_conv_avoid = ['#', '%', '&', '{', '}', '\\', '<', '>' , '*', '?', '/', '$', '!', '\'', '\"', ':', '@', '+', '|', '=']

dummy_name = ''
for i in movie_name:
    if i in file_name_conv_avoid:
        dummy_name = dummy_name + '_'
    else:
        dummy_name = dummy_name + i

movie_name = dummy_name
filename = movie_name + '.html'
f = open(filename , 'wb')
f.write(content)
f.close
# closing the file after saving it in html format
print(movie_name, 'Crawling Completed.... Successfully downloaded HTML file \n')

recurse_movie(filename)


