# Advantek Laboratories – Test Assignment

Welcome! This is a small coding challenge for potential student collaborators at Advantek Laboratories.

We focus on solving real-world problems quickly and clearly, using prototypes to validate ideas before scaling. This exercise is designed to test your Python skills, problem-solving ability, and willingness to think beyond pure coding.

---

## 🔍 Assignment: Build a Simple Exchange Rate Tracker + Recommendation Tool

### 🧠 Goal
Create a small Python command-line application that:

1. **Downloads the historical rates**
2. **Fetches today's EUR/HUF exchange rate** from a public source
3. **Appends the result** into a local `rates.csv` file
4. **Calculates a trading signal** any recognized signal type is sufficent that you find online
5. **Provides a basic trading recommendation** based on the calculated signal

---

## ✅ Requirements

- **Web scraping**:
  - Use any reliable public site
  - Handle simple errors (e.g., network issues).

- **Data storage**:
  - Store results in a local CSV file (`rates.csv`).
  - Each entry should include: date, exchange rate.

- **Command-line usage**:
  ```bash
  $ python exchanger.py fetch
  [✔] Stored rate: 388.23 HUF/EUR on 2025-04-25

  $ python exchanger.py recommend
  📊 7-day Moving Average: 387.50
  📈 Today's Rate: 388.23
  💡 Recommendation: BUY EUR
  ```

- **Clean, readable code**:
  - Modular structure
  - Meaningful comments where necessary

---

## 🌟 Bonus (Optional)

- Add a `--help` option with argument parsing
- Create simple plots (e.g., historical rates vs moving average using `matplotlib`)
- Dockerize your application (with a basic `Dockerfile`)
- Publish extra features neatly in your repo

---

## 📝 Submission

- **Fork** this repository
- Complete the assignment
- **Open a pull request** with your solution

If you cannot use GitHub for some reason, you may also email a `.zip` of your solution.

---

## ⏳ Estimated Time

The core assignment should take around **4–5 hours**.  
Bonus tasks are optional and open-ended.

---

## 🙌 Good luck, and have fun!
