import twint

# Test Twint with Elon Musk's Twitter handle
try:
    # Twint configuration
    c = twint.Config()
    c.Username = "elonmusk"  # Twitter handle for Elon Musk
    c.Store_object = True
    c.Hide_output = False  # Show output for testing purposes

    # Run Twint Lookup
    print("Fetching Twitter data for Elon Musk...")
    twint.run.Lookup(c)

    # Retrieve user data from Twint output
    user_data = twint.output.users_list[0]
    print("\n=== Elon Musk Twitter Data ===")
    print(f"Username: {user_data.username}")
    print(f"Full Name: {user_data.name}")
    print(f"Tweets: {user_data.tweets}")
    print(f"Followers: {user_data.followers}")
    print(f"Following: {user_data.following}")
    print(f"Likes: {user_data.likes}")
    print(f"Bio: {user_data.bio}")
except Exception as e:
    print(f"An error occurred: {e}")
