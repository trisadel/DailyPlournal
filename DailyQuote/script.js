const quotes = [
    { text: "Believe you can and you're halfway there.", author: "Theodore Roosevelt" },
    { text: "Push yourself, because no one else is going to do it for you.", author: "Unknown" },
    { text: "Dream it. Wish it. Do it.", author: "Unknown" },
    { text: "Don’t wait for opportunity. Create it.", author: "Unknown" },
    { text: "Great things never come from comfort zones.", author: "Unknown" }
  ];
  
  function newQuote() {
    const random = quotes[Math.floor(Math.random() * quotes.length)];
    document.getElementById("quote-text").innerText = `"${random.text}"`;
    document.getElementById("quote-author").innerText = `— ${random.author}`;
  }

  
  // Show a quote immediately when the page loads
  newQuote();