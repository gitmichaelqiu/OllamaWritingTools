from PIL import Image, ImageDraw, ImageFont

# Create a new image with a transparent background
img = Image.new('RGBA', (64, 64), color=(0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# Draw a filled circle with anti-aliasing
draw.ellipse([4, 4, 60, 60], fill=(52, 152, 219), outline=(0, 0, 0, 0))

# Load a font for better text rendering with a smaller size
font = ImageFont.truetype("arial.ttf", 20)

# Add text with better positioning and anti-aliasing
draw.text((8, 22), "OWT", fill=(255, 255, 255), font=font)

# Save the icon as PNG for better quality
img.save('icon.png', format='PNG') 