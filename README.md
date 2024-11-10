![Critter Capture (7)](https://github.com/user-attachments/assets/2908d42b-322d-4d96-b74e-ae3f0cab2ae9)

# Critter Capture

##### This project for HackRPI 2024 Urban Upgrades Unleashed is a website where you will be able to take pictures of any animals, fish, or insects that you see in your daily life. 

##### -Then it will determine the species of animal, and will provide a summary of the animal in your photo for you.

##### -You will also receive a score for the number of uploads you make, which will be shown on the leaderboard. 

##### -We have a local live map that will show the locations of the photos you have taken.

## Inspiration
Our project was originally inspired by the game Pokémon Snap. In the game, your goal is to take photographs of Pokémon, which will then get reviewed for a score.

## What it does
Our project allows a user to upload any photograph of an animal. The program will classify the animal and give the user information about this animal. This photograph will then receive a rating based on the quality of the photo. 

## How we built it
We build a classifier using a combination of HTML, CSS, PEFT Transformers, and Llava. We fine-tuned an AI model provided by Microsoft ResNet 50 on a dataset from iNaturalist to detect animal species. Our current website implements Claude to deliver an AI generated text rundown of the user's uploaded image.

## Challenges we ran into
We had a great level of difficulty in finding a suitable AI model to use. In the end, we determined to fine tune our own. We also struggled with implementing this AI into our front-end, as all of us are primarily back-end developers.

## Accomplishments that we're proud of
We fine-tuned ResNet50, which was a new experience for most of our team.

## What we learned
We learned how to fine tune an AI model. We learned how to implement multiple interesting features, such as an interactive map, uploaded image previews, and AI generated summary text.

## What's next for Critter Capture
We hope to add additional gamification to our website, and maybe build a mobile app. Depending on the popularity of our project, we will start hosting publicly instead of just on our test server.


