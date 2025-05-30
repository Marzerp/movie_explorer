testing 
#  Movie Explorer  
### A Mood-Based Movie Recommendation Tool


---

##  Overview
Movie Explorer is a Python-based app that recommends movies based on how you're feeling. By combining data from The Movie Database (TMDB) API with emotion-genre mapping techniques, it helps you find films that match your mood. Whether you're feeling happy, sad, or something in between, Movie Explorer offers personalized suggestions—while still letting you filter by genre, release year, or keywords if you want to.

---

##  Introduction  
Choosing what to watch can be surprisingly stressful, especially with so many options available. Streaming services often recommend content based on popularity or past views, but they rarely take your current emotional state into account. That’s where Movie Explorer comes in, the main idea behind this proyect is simple: help people find a movie that fits how they're feeling.

---

##  Justification  

Choosing what to watch can be hard—especially when you're just looking for something that fits your mood. Most platforms don’t let you search by how you feel, even though that’s how many people decide what to watch.

Movie Explorer tries something different: to use emotions as the starting point. It helps cut down decision time, gives more personal suggestions, and recognizes that movies often make us feel more than one thing—based on real opinions, not just genres.

---

##  What This Project Tries to Do

Here’s what the project is aiming for:

- Match Moods to Movies: We’ve linked common emotions (like joy, sadness, fear, etc.) to movie genres, based on thousands of reviews from TMDB. This helps the app suggest films that align with your mood without without needing to scroll endlessly through lists.

- Let You Fine-Tune Results
While emotion is the starting point, you can still narrow things down by release year, keywords, or genre like on most movie sites.

- Show the Human Side of Recommendations
A lot of movies aren’t tied to just one emotion. People might feel a mix of excitement, nostalgia, or even sadness from the same film. That’s part of what makes movies powerful. This project includes those overlaps, based on real opinions from viewers, making recommendations feel more personal and interesting.

- Simple and Expandable
The app is built in Python and uses the TMDB API. It’s meant to be easy to use and modify. In the future, it could even work with emotion-detection tools or personalized mood profiles.
---

##  Installation  

### Requirements
- Python 3.10  
- A free API key from TMDB (get it by clicking this link  https://www.themoviedb.org/settings/api) 

### Setup Instructions  
1. **Clone the repository**  
   ```bash
   git clone https://github.com/Marzerp/movie-explorer.git
   cd movie-explorer
   ```
2. Add your TMDB API key
   - Create a .env file (use .env_example as reference) in the proyect root and add:
   API_KEY=your_api_key

3. Run the project
   ```bash
   docker-compose up --build
   ```	
4. Access the app
   - Open your browser and go to http://localhost:8080/

---

## Tecnhologies 	

- TMDB API
- Python
   - Flask
- MongoDB
- Docker and Docker Compose 
	
---

## Author 
	
This project was created by Araceli Romero, a student of Information and Communication Technologies (TICs) at UNAM, Mexico.

Movie Explorer was developed as part of the Distributed Computing course (Class of 2025), combining interests in tech, user experience, and media.

Feel free to reach out with questions, feedback, or collaboration ideas to araceliromerozerpa@gmail.com


	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
