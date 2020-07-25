

function Quiz(questions) {
    this.score = 0;
    this.questions = questions;
    this.questionIndex = 0;
}
function prevFunction()
{

quiz.questionIndex--;
console.log(this.questionIndex)
}
function nextFunction()
{
quiz.questionIndex++;
console.log(this.questionIndex)
}
/*Quiz.prototype.nextFunction = function()
{
console.log(this.questionIndex);
this.questionIndex++;
console.log(this.questionIndex);
}
Quiz.prototype.prevFunction = function()
{
console.log(this.questionIndex);
this.questionIndex--;
console.log(this.questionIndex);
}*/
 
Quiz.prototype.getQuestionIndex = function() {
    return this.questions[this.questionIndex];
}
 
Quiz.prototype.guess = function(answer) {
if(this.getQuestionIndex().isCorrectAnswer(answer)) {
        this.score++;
    }
 
    this.questionIndex++;
console.log(this.questionIndex);
}

Quiz.prototype.isEnded = function() {
    return this.questionIndex === this.questions.length;
}
 
 
function Question(text, choices, answer) {
    this.text = text;
    this.choices = choices;
    this.answer = answer;
}
 
Question.prototype.isCorrectAnswer = function(choice) {
    return this.answer === choice;
}
 
 
function populate() {
    if(quiz.isEnded()) {
        showScores();
    }
    else {
        // show question
        var element = document.getElementById("question");
        element.innerHTML = quiz.getQuestionIndex().text;
 
        // show options
        var choices = quiz.getQuestionIndex().choices;
        for(var i = 0; i < choices.length; i++) {
            var element = document.getElementById("choice" + i);
            element.innerHTML = choices[i];
            guess("btn" + i, choices[i]);
        }
 
        showProgress();
    }
};
 
function guess(id, guess) {
    var button = document.getElementById(id);
    button.onclick = function() {
        quiz.guess(guess);
        populate();
    }
};
 
 // keeps count of current question number
function showProgress() {
    var currentQuestionNumber = quiz.questionIndex + 1;
    var element = document.getElementById("progress");
    element.innerHTML = "Question " + currentQuestionNumber + " of " + quiz.questions.length;
};
 // displays score
function showScores() {
    var gameOverHTML = "<h1>Your Result is here!</h1>";
    gameOverHTML += "<h2 id='score'> Your score: " + quiz.score + "</h2>"; // result
    var element = document.getElementById("quiz");
    element.innerHTML = gameOverHTML;
};
 
// Have to collect questions and answers data from database 
var questions = [
    new Question("Q1?", ["JavaScript", "XHTML","CSS", "HTML"], "HTML"),
    new Question("Q2", ["HTML", "JQuery", "CSS", "XML"], "CSS"),
    new Question("Q3", ["Python Script", "JQuery","Django", "NodeJS"], "Django"),
    new Question("Q4", ["PHP", "HTML", "JS", "All"], "PHP"),
    new Question("Q5", ["Web Design", "Graphic Design", "SEO & Development", "All"], "All")
];
 
var quiz = new Quiz(questions);
 
// to display quiz questions
populate();
