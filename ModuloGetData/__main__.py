from .GetReviews import get_reviews
from .InsertMovie import insert_reviews

if __name__ == "__main__":
    reviews = get_reviews()
    print(reviews)

if __name__ == "__main__":
    insert_reviews()
