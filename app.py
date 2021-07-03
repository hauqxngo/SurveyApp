from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []

@app.route('/')
def index():
    """Show homepage."""
    
    return render_template('index.html', survey=survey)

@app.route('/questions/<int:qnum>', methods=['GET', 'POST'])
def show_question(qnum):
    """Show current question."""

    # if (responses is None):
    #     return redirect('/')

    if (len(responses) == len(survey.questions)):
        return redirect('/complete')

    if (len(responses) != qnum):
        flash(f'Invalid question number: {qnum}.')
        return redirect(f'/questions/{len(responses)}')

    question = survey.questions[qnum]
    return render_template('question.html', question_num=qnum, question=question)

@app.route('/answer', methods=['POST'])
def handle_question():
    """Save response and redirect to next question."""

    # get the response choice
    choice = request.form['answer']

    # append the answer to responses list
    responses.append(choice)

    if (len(responses) == len(survey.questions)):
        return redirect('/complete')
    else:
        return redirect(f'/questions/{len(responses)}')

@app.route('/complete')
def complete():
    """Survey complete. Show Thank You page"""

    return render_template('complete.html')


