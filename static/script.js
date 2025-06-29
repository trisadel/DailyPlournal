const quotes = [
    { text: "Believe you can and you're halfway there.", author: "Theodore Roosevelt" },
    { text: "Push yourself, because no one else is going to do it for you.", author: "Unknown" },
    { text: "Dream it. Wish it. Do it.", author: "Unknown" },
    { text: "Don’t wait for opportunity. Create it.", author: "Unknown" },
    { text: "Great things never come from comfort zones.", author: "Unknown" },
    { text: "People leave, memories stay.", author: "Unknown" },
    { text: "Change is scary, but change is growth.", author: "Unknown" },
    { text: "Be with someone who makes you happy.", author: "Unknown" },
    { text: "Go after dreams not people.", author: "Unknown" },
    { text: "Happiness is not about getting all you want, It is about enjoying all you have.", author: "Unknown" },
    { text: "Happiness is not about getting all you want, it is about enjoying all you have.", author: "Unknown" },
    { text: "Do not wait for the perfect moment. Take the moment and make it perfect.", author: "Unknown" },
    { text: "Life is short. Smile while you still have teeth.", author: "Unknown" },
    { text: "Difficult roads often lead to beautiful destinations.", author: "Unknown" },
    { text: "The best view comes after the hardest climb.", author: "Unknown" },
    { text: "Don’t count the days, make the days count.", author: "Muhammad Ali" },
    { text: "Believe you can and you're halfway there.", author: "Theodore Roosevelt" },
    { text: "Success is not final, failure is not fatal: it is the courage to continue that counts.", author: "Winston Churchill" },
    { text: "In the middle of every difficulty lies opportunity.", author: "Albert Einstein" },
    { text: "You are never too old to set another goal or to dream a new dream.", author: "C.S. Lewis" },
    { text: "Do what you can, with what you have, where you are.", author: "Theodore Roosevelt" },
    { text: "Don’t watch the clock; do what it does. Keep going.", author: "Sam Levenson" },
    { text: "You don’t have to be great to start, but you have to start to be great.", author: "Zig Ziglar" },
    { text: "Dream big and dare to fail.", author: "Norman Vaughan" },
    { text: "Act as if what you do makes a difference. It does.", author: "William James" },
    { text: "Keep your face always toward the sunshine—and shadows will fall behind you.", author: "Walt Whitman" },
    { text: "What lies behind us and what lies before us are tiny matters compared to what lies within us.", author: "Ralph Waldo Emerson" },
    { text: "It does not matter how slowly you go as long as you do not stop.", author: "Confucius" },
    { text: "Every day may not be good, but there's something good in every day.", author: "Unknown" },
    { text: "Happiness is not something ready made. It comes from your own actions.", author: "Dalai Lama" },
    { text: "Be the change that you wish to see in the world.", author: "Mahatma Gandhi" },
    { text: "The only way to do great work is to love what you do.", author: "Steve Jobs" },
    { text: "Success is how high you bounce when you hit bottom.", author: "George S. Patton" },
    { text: "Everything you’ve ever wanted is on the other side of fear.", author: "George Addair" },
    { text: "The harder you work for something, the greater you’ll feel when you achieve it.", author: "Unknown" },
    { text: "Push yourself, because no one else is going to do it for you.", author: "Unknown" },
    { text: "Sometimes we’re tested not to show our weaknesses, but to discover our strengths.", author: "Unknown" },
    { text: "Great things never come from comfort zones.", author: "Unknown" },
    { text: "Don’t stop when you’re tired. Stop when you’re done.", author: "Unknown" },
    { text: "Wake up with determination. Go to bed with satisfaction.", author: "Unknown" },
    { text: "Little things make big days.", author: "Unknown" },
    { text: "Success doesn’t just find you. You have to go out and get it.", author: "Unknown" },
    { text: "Dream it. Wish it. Do it.", author: "Unknown" },
    { text: "Sometimes later becomes never. Do it now.", author: "Unknown" },
    { text: "If you want it, work for it.", author: "Unknown" },
    { text: "Great things never come from comfort zones.", author: "Unknown" },
    { text: "Stay positive. Work hard. Make it happen.", author: "Unknown" },
    { text: "Don’t limit your challenges. Challenge your limits.", author: "Unknown" },
    { text: "Doubt kills more dreams than failure ever will.", author: "Suzy Kassem" },
    { text: "Your limitation—it’s only your imagination.", author: "Unknown" },
    { text: "Discipline is the bridge between goals and accomplishment.", author: "Jim Rohn" },
    { text: "Work hard in silence, let your success be the noise.", author: "Frank Ocean" },
    { text: "Make each day your masterpiece.", author: "John Wooden" },
    { text: "Do something today that your future self will thank you for.", author: "Sean Patrick Flanery" },
    { text: "The secret of getting ahead is getting started.", author: "Mark Twain" },
    { text: "You miss 100% of the shots you don’t take.", author: "Wayne Gretzky" },
    { text: "Opportunities don't happen. You create them.", author: "Chris Grosser" },
    { text: "Success usually comes to those who are too busy to be looking for it.", author: "Henry David Thoreau" },
    { text: "If you really look closely, most overnight successes took a long time.", author: "Steve Jobs" },
    { text: "Try not to become a man of success. Rather become a man of value.", author: "Albert Einstein" },
    { text: "Life is 10% what happens to us and 90% how we react to it.", author: "Charles R. Swindoll" },
    { text: "Success is not how high you have climbed, but how you make a positive difference to the world.", author: "Roy T. Bennett" },
    { text: "The future depends on what you do today.", author: "Mahatma Gandhi" },
    { text: "The only limit to our realization of tomorrow is our doubts of today.", author: "Franklin D. Roosevelt" },
    { text: "Don’t be pushed around by the fears in your mind. Be led by the dreams in your heart.", author: "Roy T. Bennett" },
    { text: "Everything you can imagine is real.", author: "Pablo Picasso" },
    { text: "Turn your wounds into wisdom.", author: "Oprah Winfrey" },
    { text: "You don’t find the happy life. You make it.", author: "Camilla Eyring Kimball" },
    { text: "Success is getting what you want. Happiness is wanting what you get.", author: "Dale Carnegie" },
    { text: "You only live once, but if you do it right, once is enough.", author: "Mae West" },
    { text: "Happiness is not a goal... it's a by-product of a life well lived.", author: "Eleanor Roosevelt" },
    { text: "Go confidently in the direction of your dreams. Live the life you have imagined.", author: "Henry David Thoreau" },
    { text: "Do not go where the path may lead, go instead where there is no path and leave a trail.", author: "Ralph Waldo Emerson" },
    { text: "Happiness depends upon ourselves.", author: "Aristotle" },
    { text: "Stay away from those people who try to disparage your ambitions.", author: "Mark Twain" },
    { text: "We can do anything we want to if we stick to it long enough.", author: "Helen Keller" },
    { text: "Happiness is a direction, not a place.", author: "Sydney J. Harris" },
    { text: "A year from now you may wish you had started today.", author: "Karen Lamb" },
    { text: "To live a creative life, we must lose our fear of being wrong.", author: "Joseph Chilton Pearce" },
    { text: "Don’t wait. The time will never be just right.", author: "Napoleon Hill" },
    { text: "We become what we think about.", author: "Earl Nightingale" },
    { text: "Act as though it were impossible to fail.", author: "Dorothea Brande" },
    { text: "Success is not in what you have, but who you are.", author: "Bo Bennett" },
    { text: "It always seems impossible until it’s done.", author: "Nelson Mandela" },
    { text: "If opportunity doesn’t knock, build a door.", author: "Milton Berle" },
    { text: "When you know what you want, and want it bad enough, you’ll find a way to get it.", author: "Jim Rohn" },
    { text: "Courage doesn’t always roar. Sometimes courage is the quiet voice at the end of the day saying, ‘I will try again tomorrow.’", author: "Mary Anne Radmacher" },
    { text: "Limit your 'always' and your 'nevers'.", author: "Amy Poehler" },
    { text: "Nothing will work unless you do.", author: "Maya Angelou" },
    { text: "There is nothing impossible to they who will try.", author: "Alexander the Great" },
    { text: "You don’t need to see the whole staircase, just take the first step.", author: "Martin Luther King Jr." },
    { text: "The only way to achieve the impossible is to believe it is possible.", author: "Charles Kingsleigh (Alice in Wonderland)" },
    { text: "Just keep going. Everybody gets better if they keep at it.", author: "Ted Williams" },
    { text: "When you feel like quitting, think about why you started.", author: "Unknown" },
    { text: "Success is walking from failure to failure with no loss of enthusiasm.", author: "Winston Churchill" },
    { text: "Energy and persistence conquer all things.", author: "Benjamin Franklin" },
    { text: "A goal without a plan is just a wish.", author: "Antoine de Saint-Exupéry" },
    { text: "It’s never too late to be what you might have been.", author: "George Eliot" },
    { text: "Don’t let yesterday take up too much of today.", author: "Will Rogers" },
    { text: "Be so good they can’t ignore you.", author: "Steve Martin" },
    { text: "Don’t raise your voice, improve your argument.", author: "Desmond Tutu" },
    { text: "You cannot swim for new horizons until you have courage to lose sight of the shore.", author: "William Faulkner" },
    { text: "Great minds discuss ideas; average minds discuss events; small minds discuss people.", author: "Eleanor Roosevelt" },
    { text: "All our dreams can come true, if we have the courage to pursue them.", author: "Walt Disney" },
    { text: "Your time is limited, don’t waste it living someone else’s life.", author: "Steve Jobs" },
    { text: "Perseverance is not a long race; it is many short races one after the other.", author: "Walter Elliot" },
    { text: "Strive not to be a success, but rather to be of value.", author: "Albert Einstein" },
    { text: "Opportunity is missed by most people because it is dressed in overalls and looks like work.", author: "Thomas Edison" },
    { text: "Only those who dare to fail greatly can ever achieve greatly.", author: "Robert F. Kennedy" }
  ];
  
  function newQuote() {
    const random = quotes[Math.floor(Math.random() * quotes.length)];
    document.getElementById("quote-text").innerText = `"${random.text}"`;
    document.getElementById("quote-author").innerText = `— ${random.author}`;
  }

  
  // Show a quote immediately when the page loads
  newQuote();
    // dark mode
  document.addEventListener("DOMContentLoaded",() => {
    const toggleBtn = document.getElementById("darkModeToggle");
    const body = document.body;

    // load saved theme
    if (localStorage.getItem("theme") === "dark") {
      body.classList.add("dark-mode");
    }

    toggleBtn?.addEventListener("click", () => {
      body.classList.toggle("dark-mode");

      //save theme to local stogage
      localStorage.setItem("theme", body.classList.contains("dark-mode") ? "dark" : "light" );  
    })
  })