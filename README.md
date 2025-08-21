# Yoga Bot
Yoga bot is a Telegram bot for learning yoga theory. It has multiple tests with different structures for the most effective studying.

## Features
  • **Tests:** Yes/No, Open questions, Fill the gap, ABC quiz, Put in correct order, True/False  
  • **Pose detection:** an AI-trained model detects the name of the pose sent by the user and tells its key points  
  • **Broadcast message:** sending broadcast messages about updates for all users who previously interacted with the bot  

## Model choice
I chose **Logistic Regression** over **Decision Tree** because:  
  - I can have linear rules (based on angle values)  
  - I don't need a clear explanation of why the algorithm has chosen the given pose, I only need a result  
  _Note: A decision tree could be useful for correcting specific pose angles_  
  
I chose **Logistic Regression** over **KNN** because:  
  - KNN with default parameters (k=5) gave a worse accuracy of ~0.89 (for logistic regression we don't need to adjust any parameters manually)  
  - For further development, such as adding more pos
es, KNN would be less effective and slower  
  
For more details on comparing these three AI models, test results, and the decision tree graph, check the documentation folder.

## Dataset
The dataset consists of three angle measurements per sample (arms straight, left leg, right leg), each labeled with a yoga pose.

## Results
Achieved 100% accuracy on test data using logistic regression.  
KNN and decision tree models were tested for comparison, but logistic regression performed best overall.

## How to Use

1. **Download Telegram**  
   Install the Telegram app on your phone or desktop if you don’t have it already.

2. **Open the Bot**  
   Click [this link](https://t.me/yoga_learn_bot) to open **Yoga Bot** in Telegram.

3. **Start Conversation**  
   Send /start or click the “Start” button below. Use the commands in the start message to take the tests or send a yoga photo and receive an instant pose prediction.

4. **Get Feedback**  
   The bot will reply with the results of the test, explanations, or the detected yoga pose based on your image.

## Deployment

**Yoga Bot is deployed on [Railway](https://railway.app/)**  
It provides 24/7 availability of the bot, with no setup required from the user.

## Demo

A short YouTube video demonstrating all features is [here](https://youtu.be/CDPF8k34Lc8).
## APIs and Libraries Used

- **MediaPipe** – For extracting pose landmarks from images  
- **scikit-learn** – For building and comparing machine learning models  
- **Telegram Bot API** – For handling bot-user interactions  
- **OpenCV** – For image reading and preprocessing  
- **Matplotlib** – For optional visualization of poses (during development)  
- **pandas** – For working with the dataset and model training

## Installation

### Using Docker

1. Make sure you have Docker installed.  
   [Get Docker](https://docs.docker.com/get-docker/)

2. Clone this repository:

   ```bash
   git clone https://github.com/your-username/yoga-bot.git
   cd yoga-bot
3. Build and run the bot:
   
   ```bash
    docker build -t yoga-bot .
    docker run -d --name yoga_bot_container yoga-bot

The bot will now be running in the background and ready to receive Telegram messages.













