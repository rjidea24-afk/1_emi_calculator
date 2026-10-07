from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    emi = None
    total_interest = None
    total_payment = None
    error = None

    if request.method == 'POST':
        try:
            principal = float(request.form['principal'])
            rate = float(request.form['rate'])
            tenure_value = float(request.form['tenure'])
            tenure_type = request.form['tenure_type']

            # अगर Tenure वर्षों में है तो उसे महीनों में बदलें
            if tenure_type == 'years':
                tenure_months = tenure_value * 12
            else:
                tenure_months = tenure_value

            if principal > 0 and rate > 0 and tenure_months > 0:
                # मासिक ब्याज दर
                monthly_rate = (rate / 12) / 100
                
                # EMI फॉर्मूला: P * r * (1 + r)^n / ((1 + r)^n - 1)
                emi_val = principal * monthly_rate * ((1 + monthly_rate) ** tenure_months) / (((1 + monthly_rate) ** tenure_months) - 1)
                
                total_pay = emi_val * tenure_months
                tot_interest = total_pay - principal

                emi = round(emi_val, 2)
                total_payment = round(total_pay, 2)
                total_interest = round(tot_interest, 2)
            else:
                error = "कृपया सही और सकारात्मक मान (Positive Values) दर्ज करें।"
        except Exception as e:
            error = "गणना में कोई त्रुटि हुई। कृपया इनपुट की जाँच करें।"

    return render_template('index.html', emi=emi, total_interest=total_interest, total_payment=total_payment, error=error)

if __name__ == '__main__':
    app.run(debug=True)