from flask import Flask, request, render_template, redirect, flash, session, make_response
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys

app=Flask(__name__)

app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

respond = "responses"
current = "current_survey"
#session keys


@app.route("/")
def pick_a_survey():
    """display pick_a_survey page"""
    return render_template("pick_a_survey.html", surveys=surveys )

@app.route('/', methods=["POST"])
def survey_selection():
    """ home page for the Survey"""
    survey_id =request.form['survey_num']
    survey = surveys[survey_id]
    session[current] = survey_id
    return render_template("root.html",survey=survey,qnum = len(survey.questions))

@app.route("/start_survey", methods=["POST"])
def start_survey():
    """Clear responses list"""
    session[respond] = []
    return redirect("/questions/0")

@app.route("/questions/<int:questionid>")
def show_question(questionid):
    """Display Questions 1 at a time"""
    responses =session.get(respond)
    survey_num = session[current]
    survey = surveys[survey_num]

    if (responses is None):
        # redirect to home page if no no response to question
        return redirect("/")

    if (len(responses) == len(survey.questions)):
        # All questions answered go to Thank you page.
        return redirect("/complete")

    if (len(responses) != questionid):
        # redirect back to proper question if URL is tappered with.
        flash(f"INVALID QUESTION ID: {questionid}.")
        return redirect(f"/questions/{len(responses)}")

    question = survey.questions[questionid]
    return render_template("questions.html", question_num=questionid, question=question )


@app.route("/answer", methods=["POST"])
def handle_question():
    """Save answer to responses list and continue to next question."""

    # get the answer chosen
    choice = request.form['answer']

    # save  answer in the responses list
    responses = session[respond]
    responses.append(choice)
    session[respond] = responses
    survey_num = session[current]
    survey = surveys[survey_num]


    if (len(responses) == len(survey.questions)):
        # survey completed.  direct to thank you page
        return redirect("/complete")

    else:
        return redirect(f"/questions/{len(responses)}")

@app.route("/complete")
def complete():
    """ Thank them for completing the survey."""
    survey_id = session[current]
    survey = surveys[survey_id]
    responses= session[respond]
    return render_template("complete.html",survey=survey,rep=session.get(respond) )