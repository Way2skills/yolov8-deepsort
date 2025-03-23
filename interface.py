from src.marine_detect.predict import predict_on_images, predict_on_video

def validate_args(models, confs):
    """Ensure models and confidence thresholds have matching lengths"""
    if len(models) != len(confs):
        raise ValueError("Number of models and confidence thresholds must match")

def main():
    print("Welcome to the Marine Object Detection CLI!")
    print("Choose a mode:")
    print("1. Process Images")
    print("2. Process Video")
    mode = input("Enter your choice (1 or 2): ").strip()

    if mode not in ["1", "2"]:
        print("Invalid choice. Exiting.")
        return

    # Default models
    default_models = ["FishInv.pt", "MegaFauna.pt"]
    default_confs = [0.522, 0.6]

    # Get model paths
    models_input = input(
        f"Enter model paths (space-separated, default: {', '.join(default_models)}): "
    ).strip()
    models = models_input.split() if models_input else default_models

    # Get confidence thresholds
    confs_input = input(
        f"Enter confidence thresholds (space-separated, default: {', '.join(map(str, default_confs))}): "
    ).strip()
    confs = list(map(float, confs_input.split())) if confs_input else default_confs

    try:
        validate_args(models, confs)
        if mode == "1":
            input_folder = input("Enter the input folder path for images: ").strip()
            output_folder = input("Enter the output folder path for results: ").strip()
            predict_on_images(
                model_paths=models,
                confs_threshold=confs,
                images_input_folder_path=input_folder,
                images_output_folder_path=output_folder
            )
        elif mode == "2":
            input_video = input("Enter the input video file path: ").strip()
            output_video = input("Enter the output video file path: ").strip()
            predict_on_video(
                model_paths=models,
                confs_threshold=confs,
                input_video_path=input_video,
                output_video_path=output_video
            )
        print("Processing complete!")
    except ValueError as e:
        print(f"Error: {str(e)}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()