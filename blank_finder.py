from PIL import Image, ImageStat
import cv2
import os
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

def adjust_brightness(image, target_brightness):
    stat = ImageStat.Stat(image)
    brightness = sum(stat.mean) / len(stat.mean)
    ratio = target_brightness / brightness
    adjusted = image.point(lambda p: p * ratio)
    return adjusted

def crop_image(image, crop_box):
    rotated_image = image.rotate(180)
    return rotated_image.crop(crop_box)

def save_image(image, title):
    folder_name = datetime.now().strftime("%Y%m%d_%H%M%S")
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    file_path = os.path.join(folder_name, f"{title.replace(' ', '_').lower()}.png")
    plt.figure(figsize=(8, 8))
    plt.imshow(image)
    plt.title(title)
    plt.axis('off')
    plt.savefig(file_path)
    plt.close()

def background_subtraction_with_enhanced_probability_overlay(background_image, object_image, img_name, q):
    background = np.array(background_image.convert('RGB'))
    object_image = np.array(object_image.convert('RGB'))
    
    background = cv2.cvtColor(background, cv2.COLOR_RGB2BGR)
    object_image = cv2.cvtColor(object_image, cv2.COLOR_RGB2BGR)
    
    background = cv2.resize(background, (640, 480))
    object_image = cv2.resize(object_image, (640, 480))
    
    blurred_background = cv2.GaussianBlur(background, (101, 101), 0)
    blurred_object_image = cv2.GaussianBlur(object_image, (101, 101), 0)
    
    diff_image = cv2.absdiff(blurred_background, blurred_object_image)
    gray_diff = cv2.cvtColor(diff_image, cv2.COLOR_BGR2GRAY)
    
    _, thresh = cv2.threshold(gray_diff, 30, 255, cv2.THRESH_BINARY)
    
    h, w = thresh.shape
    h_half, w_half = h // 2, w // 2
    
    sections = [thresh[:h_half, :w_half], thresh[h_half:, :w_half], thresh[:h_half, w_half:], thresh[h_half:, w_half:]]
    probabilities = [np.sum(section) / section.size for section in sections]
    display_image = object_image.copy()
    
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    font_color = (255, 0, 0)
    font_thickness = 2
    
    positions = [(w_half // 2, h_half // 2), (w_half // 2, 3 * h_half // 2),
                 (3 * w_half // 2, h_half // 2), (3 * w_half // 2, 3 * h_half // 2)]
    
    for pos, prob in zip(positions, probabilities):
        cv2.putText(display_image, f'{prob:.2f}', pos, font, font_scale, font_color, font_thickness)
    save_image(cv2.cvtColor(display_image, cv2.COLOR_BGR2RGB), f'Enhanced Probability Overlay {img_name}')
    
    q.put(probabilities)    # queue에 넣어서 나중에 음식 투입 시 빈칸 정보 불러옴(thread간 데이터 공유)
    return probabilities

def blank_finder(image_path, q):
    # print(f"This module's name: {__name__}")
    background_image_path = "./refridge_images/background.jpg"
    crop_box = (74, 202, 458, 450)
    background_gt = Image.open(background_image_path)
    cropped_background_gt = crop_image(background_gt, crop_box)
    save_image(cropped_background_gt, 'Cropped Background')
    stat_background = ImageStat.Stat(cropped_background_gt)
    brightness_background = sum(stat_background.mean) / len(stat_background.mean)
    all_probabilities = []
    image = Image.open(image_path)
    cropped_image = crop_image(image, crop_box)
    save_image(cropped_image, f'Cropped Object Image')
    stat = ImageStat.Stat(cropped_image)
    brightness = sum(stat.mean) / len(stat.mean)
    if brightness < brightness_background:
        adjusted_image = adjust_brightness(cropped_image, brightness_background)
        save_image(adjusted_image, f'Brightness Adjusted Object Image')
        probabilities = background_subtraction_with_enhanced_probability_overlay(cropped_background_gt, adjusted_image, f'Image', q)
    else:
        adjusted_background = adjust_brightness(cropped_background_gt, brightness)
        save_image(adjusted_background, f'Brightness Adjusted Background Image')
        probabilities = background_subtraction_with_enhanced_probability_overlay(adjusted_background, cropped_image, f'Image', q)
    all_probabilities.append(probabilities)
    return all_probabilities  # Return the list of probability arrays for all images
