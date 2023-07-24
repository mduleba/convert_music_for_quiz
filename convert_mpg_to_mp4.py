from moviepy.editor import VideoFileClip


def convert_mpg_to_mp4(mpg_file_path, output_file_path):
    clip = VideoFileClip(mpg_file_path)
    clip.write_videofile(output_file_path, codec='libx264', audio_codec='aac')


if __name__ == "__main__":
    mpg_file_path = r"M:\Superbaloo\bajki.mpg"  # Replace with your .mpg file path
    output_file_path = r"M:\Superbaloo\superbaloo_full_v2.mp4"  # Replace with your desired output .mp4 file path
    convert_mpg_to_mp4(mpg_file_path, output_file_path)
