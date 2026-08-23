This bot automatically solves the daily wordle for you.
We use Python along with Playwright, a powerful web automation library. Playwright is perfect for this because it easily bypasses the pop-ups on the New York Times website and simulates real keyboard strokes.
This is a complete Python script that automatically fetches a standard Wordle word list, opens the browser, interacts with the game, reads the tile colors, and filters out the wrong words until it solves the puzzle.

Steps to use:
1. Open your terminal and use pip to install playwright.
2. Use playwright to install chromium.
3. The commands to do the same are as follows:
 **pip install playwright**
**playwright install chromium**
5. Create a folder on your desktop and place the .py file in it.
6. Right click the folder and open it in terminal.
7. Simply use the command:
**python wordle_bot.py**

The bot will automatically download the list of all possible 5-letter words from github and open the site.
It will then wait for you to dismiss all pop-ups and click Enter on the terminal.
Then it will automatically start guessing words starting with the statistically most-effective word "Crane" and noting every letters status in brackets as Correct, Given or Empty for Green, Yellow and Grey respectively.
This process repeats until it correctly guesses the word.
Once done, it keeps the site open for 10 seconds for you to share your result before it automatically closes it.
