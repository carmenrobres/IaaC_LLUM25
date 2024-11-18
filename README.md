# IaaC_LLUM25 City Image Generator

This project provides a web-based interface for generating and displaying city images using an AI model. The system integrates a FastAPI backend with a frontend interface that updates dynamically based on user input.
Forked from [Jorge's Repo](https://github.com/jmuozan/IaaC_LLUM25)
## Features
- Generates images based on AI prompts and displays them in a web interface.
- Real-time updates using WebSockets for a responsive user experience.
- Typewriter effect for displaying prompts on the webpage.
- Automatically refreshes the displayed image when a new one is generated.

## Project Structure
- **`index.html`**: Frontend interface that displays the generated image and user prompts.
- **`app_display.py`**: Backend FastAPI application managing the prompt input and WebSocket communication.
- **`main.py`**: Main script that handles image generation using OpenAI API (not provided, assumed to be implemented by you).
- **Static Files**: Contains the generated images in the `static/Generated_Images/` directory.

## Prerequisites
- Python 3.8 or higher
- OpenAI API Key

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/carmenrobres/IaaC_LLUM25.git
   cd IaaC_LLUM25
  ```

2. Set up a virtual environment and install dependencies:

   ```bash
   python3 -m venv env
   source env/bin/activate   # On macOS/Linux
   .\env\Scripts\activate    # On Windows
   pip install -r requirements.txt
   ```
3. Create a .env file in the root directory and add your OpenAI API key:
   ```bash
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## Running the Application
1. Start the main image generation script:
   ```bash
   python main.py
   ```
2. In a separate terminal, run the FastAPI application:
   ```bash
   python -m uvicorn app_display:app --reload
   ```
3. Open your web browser and go to:
  ```bash
   http://127.0.0.1:8000
  ```
## Usage
- The left panel of the interface displays the prompts in a typewriter style.
- The right panel shows the latest generated image.
- New sentences can be added using a form (handled by the backend).
- The image reloads automatically whenever a new image is generated.

## Known Issues

- **Image Update Issue**: The image is reloaded using a timestamp to prevent caching issues (`reloadImage()` function in `index.html`). However, if a new image is not generated in the `static/Generated_Images` folder, the displayed image may not update properly. Ensure the image file is updated by the `main.py` script.

- **Prompt Box Limit**: Currently, there is no limit on the number of prompt boxes shown on the left panel. This can be resolved by modifying the `notify_clients()` function in `app_display.py` to limit the number of displayed sentences.

## Future Enhancements

- Add transition animations for smoother UI updates.
- Limit the number of displayed prompts to prevent overflow.
- Integrate additional movement and visual effects for improved user experience.

## Troubleshooting

- If you encounter a **WebSocket connection error**, ensure both the FastAPI server and the `main.py` script are running correctly.
- If the image is not updating, try clearing the browser cache or ensure the image file is being updated correctly in the `static/Generated_Images/` folder.
