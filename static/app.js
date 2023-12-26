class Boggle {
    constructor(gameId, secs = 60){
        this.secs = secs;
        this.showTimer();
        this.score = 0;
        this.words = new Set();
        this.board = $("#" + gameId);
        //Using bind, the timer changes the time left on the board each second
        this.timer = setInterval(this.tick.bind(this), 1000);
        $(".submit-word", this.board).on("submit", this.handleSubmit.bind(this));
    }

    showWord(word){
        $(`<li>${word}</li>`).appendTo($(".words", this.board));
    }

    showScore(){
        $(".score", this.board).text(this.score);
    }

    showMessage(msg, msg_type){
        $(".msg", this.board).text(msg).removeClass().addClass(`msg ${msg_type}`);
    }

    // These two functions will handle running the timer for the game

    showTimer(){
        $('.timer', this.board).text(this.secs);
    }

    async tick(){
        //Substracts one second from the timer each time it is called in setInterval in the constructor portion of the Boggle Class
        this.secs -=1;
        this.showTimer();
        //Once the timer has run out, it will stop the timer, and then score the game by calling the method scoreGame
        if(this.secs === 0){
            clearInterval(this.timer);
            await this.scoreGame();
        }
    }

    // This will be triggered by the form's button click. This method will communicate with Python and Flask to access methods from boggle class in boggle.py
    async handleSubmit(evt){
        //Each time a new word is submitted, this method fires. It will check the word for validity, flash appropriate messages, and adjust score when necessary.
        evt.preventDefault();
        const $new_word = $('#new_word', this.board);
        let new_word = $new_word.val();
        if(!new_word){
            return;
        }
        //Shows an error message when the user submits a word that has already successfully been added.
        if(this.words.has(new_word)){
            this.showMessage(`Oops! You already found ${new_word}.`, "error");
            return;
        }

        //This is where the app accesses the Python and Flask and checks the words for validity
        const response = await axios.get('/check-word', { params :{new_word: new_word}})
        if(response.data.result === "not-word"){
            this.showMessage(`Sorry. ${new_word.toUpperCase()} is not a valid English word.`, 'error');
        } else if (response.data.result === "not-on-board"){
            this.showMessage(`Sorry. ${new_word.toUpperCase()} is not on the board.`, 'error');
        } else {
            this.showWord(new_word);
            this.score += new_word.length;
            this.showScore();
            this.words.add(new_word);
            this.showMessage(`Nice! You got ${new_word.length} points for the word: ${new_word.toUpperCase()}`, 'success');
        }

        $new_word.val("").focus();
    }

    // This final method will handle the score

    async scoreGame(){
        //Accesses python/flask through /post-score.  Sends the final score of the game. The server responds with a response that tells whether or not the user broke the highscore record.
        $(".submit-word", this.board).hide();
        const response = await axios.post("/post-score", {score: this.score});
        if(response.data.brokeRecord){
            this.showMessage(`NEW RECORD of ${this.score} points!!`, 'success');
        }
        else {
            this.showMessage(`Final score: ${this.score}`, "success");
        }
    }
}