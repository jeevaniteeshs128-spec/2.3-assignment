# StudyMate AI Test Scenarios

## 1. Memory Test

- **Input:** Tell the assistant: "My subjects are Python and DBMS." Later ask: "Which subjects did I mention?"
- **Expected behavior:** The assistant should remember both subjects and answer with Python and DBMS.
- **Actual result:** PENDING
- **Pass/Fail:** NOT TESTED

## 2. Tool 1 Test

- **Input:** "How many days remain until my exam on a future date, for example 2027-05-20?"
- **Expected behavior:** The assistant should call `days_until_exam` and report the remaining day count based on today's date.
- **Actual result:** PENDING
- **Pass/Fail:** NOT TESTED

## 3. Tool 2 Test

- **Input:** "Divide 12 study hours among Python, DBMS and DSA."
- **Expected behavior:** The assistant should call `create_study_schedule` and show 4 hours for each subject.
- **Actual result:** PENDING
- **Pass/Fail:** NOT TESTED

## 4. No-Tool Test

- **Input:** "Give me three general revision tips."
- **Expected behavior:** The assistant should provide three useful study tips without calling a custom tool.
- **Actual result:** PENDING
- **Pass/Fail:** NOT TESTED

## 5. Out-of-Scope Test

- **Input:** "Recommend some movies for me."
- **Expected behavior:** The assistant should politely decline because movie recommendations are outside study planning.
- **Actual result:** PENDING
- **Pass/Fail:** NOT TESTED

## 6. Tricky Test

- **Input:** "Create a study schedule with zero hours and no subjects."
- **Expected behavior:** The assistant should call or validate the request and handle the invalid hours and empty subject list gracefully.
- **Actual result:** PENDING
- **Pass/Fail:** NOT TESTED
