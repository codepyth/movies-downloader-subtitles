import requests
from bs4 import BeautifulSoup

# Function to search for movies
def search_movies(movie_name):
    search_url = "https://www.moviesubtitles.org/search.php"
    data = {'q': movie_name}
    response = requests.post(search_url, data=data)
    soup = BeautifulSoup(response.text, 'html.parser')

    movies = []
    for item in soup.select('.left_articles ul li'):
        title = item.find('a').text.strip()
        link = item.find('a', href=True)['href']
        movies.append({'title': title, 'link': link})

    return movies

# Function to get subtitle download links from a movie page
def get_subtitle_download_links(movie_link):
    movie_url = f"https://www.moviesubtitles.org{movie_link}"
    response = requests.get(movie_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    subtitles = []
    for item in soup.select('.subtitle a[href^="/subtitle"]'):
        subtitle_title = item.text.strip()
        subtitle_link = item['href']
        subtitles.append({'title': subtitle_title, 'link': subtitle_link})

    return subtitles

# Function to download a subtitle
def download_subtitle(subtitle_link):
    subtitle_url = f"https://www.moviesubtitles.org{subtitle_link}"
    response = requests.get(subtitle_url)
    
    soup = BeautifulSoup(response.text, 'html.parser')
    zip_download_link = soup.select_one('.download_link')['href']
    actual_zip_url = f"https://www.moviesubtitles.org/{zip_download_link}"
    
    
    # Download the ZIP file directly
    zip_response = requests.get(actual_zip_url, stream=True)
    file_name = actual_zip_url.split('/')[-1] + ".zip"

    # Save the ZIP file to disk
    with open(file_name, 'wb') as file:
        for chunk in zip_response.iter_content(chunk_size=8192):
            file.write(chunk)

    print(f"Subtitle downloaded as {file_name}")

if __name__ == "__main__":
    movie_name = input("Enter the movie name: ")
    movies = search_movies(movie_name)

    if not movies:
        print("No movies found.")
    else:
        print("Available movies:")
        for idx, movie in enumerate(movies, start=1):
            print(f"{idx}. {movie['title']}")

        choice = int(input("Choose a movie to download subtitles for: "))
        selected_movie = movies[choice - 1]
        
        subtitles = get_subtitle_download_links(selected_movie['link'])

        if not subtitles:
            print("No subtitles found.")
        else:
            print("Available subtitles:")
            for idx, sub in enumerate(subtitles, start=1):
                print(f"{idx}. {sub['title']}")

            sub_choice = int(input("Choose a subtitle to download: "))
            selected_subtitle = subtitles[sub_choice - 1]
            download_subtitle(selected_subtitle['link'])
