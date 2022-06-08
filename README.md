# SitterSocial
Simple Social Network with Django and Django rest
framework

Basic models:
- User
- Post (always made by a user)
Basic features:
- user signup
- user login
- post creation
- post like
- post unlike
- post dislike

##Requirements:

- Token authentication (JWT is prefered)

- Use clearbit.com/enrichment for getting additional data for the user on signup

- Use emailhunter.co for verifying email existence on signup.

- Automated bot that demonstrate functionalities of the system according to defined rules.
Bot reads rules from a config file where given: number_of_users, max_posts_per_user, max_likes_per_user

Bot reads the configuration and create this activity:
- signup users (number provided in config)
- each user creates random number of posts with any content (up to
max_posts_per_user)
- After creating the signup and posting activity, posts should be liked randomly, posts
could be liked multiple times.
