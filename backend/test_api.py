import pickle
import pandas as pd

with open("./model/tfidf_vectorizer.pkl", "rb") as f:
    tfidf = pickle.load(f)

with open("./model/logistic_model.pkl", "rb") as f:
    logistic_model = pickle.load(f)




test_texts = [
  " We are looking for a Senior Software Engineer to join our Bangalore development team. The "
  "candidate must have strong experience in Python, Django, and REST APIs. You will wor"
  "k closely with product managers and QA teams to deliver scalable enterprise solutions. "
  "Competitive salary, PF, health insurance, and annual bonuses provided."
      ,

    "Congratulations! You have been selected for our company. To confirm your job offer, pay 5,000 rupees as registration"
    " and training fees. Once payment is done, offer letter will be released."
    ,

    "Tata Consultancy Services is inviting applications for Business Analyst roles. Applicants must possess strong "
    "communication and analytical skills. Prior experience in financial or healthcare domains will be an added advantage."
    " Official offer letters will be issued through company email only"
    ,
    "urgent hirirng ! for  fresher the role is instagram post manager work from office and the salary is 2 lakh per month ",
    "Earn  500 per month for a full stack developer,reqired four years of experience "
]


def get_predictions(text):
    X = tfidf.transform([text])
    logi_pred = logistic_model.predict(X)[0]
   
    return logi_pred

results = []

for text in test_texts:
    logi, nb = get_predictions(text)
    results.append([text[:55], logi, nb])

df = pd.DataFrame(results, columns=["Input Text", "Logistic", "NaiveBayes"])

print("\nTesting API:\n")
print(df.to_string(index=False))
