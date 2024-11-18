from scripts.audioprocessor import AudioProcessor
from scripts.transcribe_audio import transcribe_audio
from scripts.image_generator import generate_image
from scripts.history_manager import update_and_get_history
import requests


def send_transcription_to_web(transcription):
    url = "http://127.0.0.1:8000/add-sentence"
    data = {"sentence": transcription}
    try:
        response = requests.post(url, data=data)
        if response.status_code == 200:
            print(f"Successfully sent transcription to the website: {transcription}")
        else:
            print(f"Failed to send transcription. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error sending transcription to website: {e}")


def process_audio(audio_processor, audio_files, transcriptions):
    # Step 1: Record and transcribe 3 times
    for i in range(3):
        audio_data = audio_processor.record_audio()
        audio_filename = f"recording_{i+1}.wav"
        audio_processor.save_audio(audio_data, audio_filename)
        audio_files.append(audio_filename)

        # Transcribe audio
        transcription = transcribe_audio(audio_filename)
        transcriptions.append(transcription)
        print(f"Transcription {i+1}: {transcription}")
        # Send transcription to the FastAPI server
        send_transcription_to_web(transcription)


    # Step 2: Store transcriptions in history.txt and prepare image prompt
    combined_text = " ".join(transcriptions)
    history = update_and_get_history(transcriptions)

    # Step 3: Generate image based on combined history
    prompt = "This is a collaborative image based on: " + ". ".join(history)
    image_path = generate_image(prompt)

    # Step 4: Merge audio files
    merged_audio_path = audio_processor.merge_audio_files(audio_files)

    print(f"Image saved at: {image_path}")
    print(f"Combined audio saved at: {merged_audio_path}")



def main():
    # Initialize components
    audio_processor = AudioProcessor()

    while True:
        transcriptions = []
        audio_files = []

        # Process audio and generate image
        process_audio(audio_processor, audio_files, transcriptions)

        # Wait for user input before continuing
        print("3 prompts processed. Type '1' to continue, or 'exit' to quit.")
        user_input = input("Enter '1' to continue or 'exit' to quit: ")
        if user_input.lower() == 'exit':
            print("Exiting the program.")
            break
        while user_input != '1':
            print("Invalid input. Please enter '1' to continue.")
            user_input = input("Enter '1' to continue or 'exit' to quit: ")
            if user_input.lower() == 'exit':
                print("Exiting the program.")
                return

if __name__ == "__main__":
    main()
