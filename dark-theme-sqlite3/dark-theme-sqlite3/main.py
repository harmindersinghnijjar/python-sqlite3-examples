import eel
import sqlite3

# Initialize Eel
eel.init('web')

# Create a connection to the SQLite database
conn = sqlite3.connect('theme.db')
c = conn.cursor()

# Create a table to store the current theme
c.execute('''CREATE TABLE IF NOT EXISTS theme
             (name text)''')

# Set the default theme to dark
c.execute("INSERT OR IGNORE INTO theme VALUES ('dark')")
conn.commit()

# Define the index page
@eel.expose
def index():
    # Retrieve the current theme from the database
    c.execute("SELECT name FROM theme")
    theme = c.fetchone()[0]

    # Render the HTML page with the current theme
    return eel.render('index.html', {'theme': theme})

# Define the function to switch themes
@eel.expose
def switch_theme():
    # Retrieve the current theme from the database
    c.execute("SELECT name FROM theme")
    theme = c.fetchone()[0]

    # Toggle the theme
    if theme == 'dark':
        new_theme = 'light'
    else:
        new_theme = 'dark'

    # Update the database with the new theme
    c.execute("UPDATE theme SET name=?", (new_theme,))
    conn.commit()

    # Reload the page with the new theme
    eel.reload()

# Run the app
eel.start('index.html', size=(400, 300))
