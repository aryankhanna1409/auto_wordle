import urllib.request
import time
import random
from playwright.sync_api import sync_playwright

print("Downloading word list...")
url = "https://raw.githubusercontent.com/tabatkins/wordle-list/master/words"
response = urllib.request.urlopen(url)
word_list = response.read().decode('utf-8').splitlines()
# Ensure all words are lowercase
possible_words = [w.lower() for w in word_list if len(w) == 5]

def filter_words(words, guess, states):
    """Filters the remaining words based on Wordle feedback."""
    filtered = []
    guess = guess.lower()
    for word in words:
        word = word.lower()
        match = True
        for i, (char, state) in enumerate(zip(guess, states)):
            if state == "correct":
                if word[i] != char: 
                    match = False
            elif state == "present":
                if char not in word or word[i] == char: 
                    match = False
            elif state == "absent":
                if char in word:
                    # Edge case: duplicate letters in a guess
                    if char not in [guess[j] for j in range(5) if states[j] != 'absent']:
                        match = False
        if match:
            filtered.append(word)
    return filtered

def main():
    with sync_playwright() as p:
        print("Launching browser...")
        browser = p.chromium.launch(headless=False) 
        page = browser.new_page()
        
        # Bypass heavy background trackers to prevent timeouts
        page.goto("https://www.nytimes.com/games/wordle/index.html", wait_until="domcontentloaded")

        # Wait for YOU to clear the screen
        print("\nBrowser is open!")
        print("1. Close the 'How to Play' and 'Log in' popups manually.")
        print("2. Click anywhere on the blank Wordle board so it has keyboard focus.")
        input("3. Press ENTER right here in the terminal to start the bot... ")
        
        global possible_words
        guess = "crane"
        
        for attempt in range(6):
            all_tiles = page.locator("div[data-testid='tile']")
            last_tile_index = (attempt * 5) + 4
            
            # 1. The Guessing Loop (Handles Rejections)
            while True:
                print(f"\nAttempt {attempt + 1}. Guessing: {guess.upper()}")
                
                page.keyboard.type(guess)
                page.keyboard.press("Enter")
                
                # Wait and watch the 5th tile to see if it gets a color
                accepted = False
                for _ in range(10): # Max wait of 5 seconds
                    last_state = all_tiles.nth(last_tile_index).get_attribute("data-state")
                    if last_state and last_state.lower() in ["correct", "present", "absent"]:
                        accepted = True
                        break
                    time.sleep(0.5)
                
                if accepted:
                    # The word was accepted and flipped! Break out of the retry loop.
                    break 
                else:
                    # The word was rejected (e.g. "Not in word list")
                    print(f"-> NYT rejected '{guess.upper()}'. Clearing row and retrying...")
                    for _ in range(5):
                        page.keyboard.press("Backspace")
                        time.sleep(0.1)
                    
                    # Remove the bad word and pick a new one
                    if guess in possible_words:
                        possible_words.remove(guess)
                    guess = random.choice(possible_words)
            
            # 2. Read the confirmed colors
            states = []
            for i in range(5):
                state_val = all_tiles.nth(attempt * 5 + i).get_attribute("data-state")
                states.append(state_val.lower() if state_val else "empty")
            
            print(f"Feedback: {states}")
            
            # 3. Check for win condition
            if all(state == 'correct' for state in states):
                print(f"\n Solved in {attempt + 1} guesses!")
                break
                
            # 4. Filter out bad words based on the colors
            possible_words = filter_words(possible_words, guess, states)
            if guess in possible_words:
                possible_words.remove(guess)
            
            if not possible_words:
                print("Uh oh, ran out of words in the dictionary!")
                break
                
            guess = random.choice(possible_words)
        
        print("\nLeaving browser open for 10 seconds so you can see the result...")
        time.sleep(10)
        browser.close()

if __name__ == "__main__":
    main()