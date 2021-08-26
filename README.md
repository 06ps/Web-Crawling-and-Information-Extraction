## Web-Crawling-and-Information-Extraction

##### Computing Lab-II (CS69012) | Spring 2021 | Guide: Prof. Animesh Mukherjee

In this project crawled RottenTomatoes website and extracted the required information from them by creating suitable grammar rules. RottenTomatoes is an IMDb like website, where one can find an online database of information related to films, television programs including cast, production crew, personal biographies, plot summaries, trivia, ratings, critic and fan reviews.
This project used "rotton tomatoes movie genre link.txt" file, which contains URL links for ten different genre-wise top 100 movie lists. Using python code, read each of the URLs and save the pages in HTML format. The user can input any of the ten genres, then the code will list all the movies in that genre and wait for user input for a particular movie name from the list. After receiving movie name as input from the user, corresponding movie page's HTML file got downloaded. After saving the movie page, created grammars using PLY to extract the following fileds for the movies:
1. Movie Name
2. Director
3. Writers
4. Producer
5. Original Language
6. Cast with the character name
7. Storyline
8. Box office collection
9. Runtime
10. You might also like - similar kind of movie suggesions
11. where to watch - Online platforms where the movie can be seen

The user can give any of the above options as an input, in return the user will be provided with choosen input information.

**Some Important Functionality**

1. You might also like - If the user give "you might also like" as an input then similar kind of movie suggestions will be printed, user can further select any of the movie from the listed suggested movies to get the same options list(above mentioned fields for movies).
2. Cast with the character member - After printing the cast members of a movie, user can input any of the listed cast member, after getting the input the profile of that particular cast member will be downloaded and will further provide the following options to the user:
  
      a. Highest Rated Film
      
      b. Lowest Rated Film
      
      c. Birthday
      
      d. His/Her other movies
  
  Then wait for the user to select from any of the above options and show the results as per selection. For "His/Her other movies", further asking for a year and using it as a filter to show all the movies on or after that year. 
  
  
  #### Commands to run the code:
  Open terminal and run the command: make
