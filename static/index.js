///////////////////////////////////////////////
//                                           //
//             Global Variables              //
//                                           //
///////////////////////////////////////////////

var compSymbol;
var humanSymbol;
var firstPlayer = "x";
var currentBoard = "---------";
var gameButtons = ["start-button", "reset-button", "simulate-button"];
var buttonFunctions = {"start-button": startGame, "reset-button": resetAI, "simulate-button": startSimulation};
var messageBoxes = ["message"];
var resetMessageStart = "Resetting AI";
var resetMessageDone = "AI Successfully Reset";
var simMode;
var numGames;
var gameNum;
var maxGamesOnline = 50;
var maxGamesBatch = 500;
var stopSim = false;
var simMessage = "Simulating Game 1";
var simMessageBatch = "Simulating";
var simMessageDone = "Simulations Complete";
var simMessageCancel = "Simulations Cancelled";
var messageInfo = document.getElementById("message-info");

///////////////////////////////////////////////
//                                           //
//              Helper Functions             //
//                                           //
///////////////////////////////////////////////

function toPercent(decimal){
	percent = Math.round(10000*decimal) / 100 + "%";
	return (percent)
}

function showMessage(msg, infoIcon, elementId){
	if (infoIcon === undefined) {
		infoIcon = false;
    }

	if (elementId === undefined) {
		elementId = "message";
    }

    if (infoIcon){
    	messageInfo.classList.remove("hidden");
    }else{
    	messageInfo.classList.add("hidden");
    }

	document.getElementById(elementId).innerHTML = msg;
}

function getBox(row, col){
	return (document.querySelectorAll("[data-row='" + row + "'][data-col='" + col + "'] span")[0]);
}

function clearMessages(messages){
	if (messages === undefined) {
		messages = messageBoxes;
    }

	if (Array.isArray(messages)){
		var messages = [messages];
	}

	for (var i=0; i < messages.length; i++){
		var message = messages[i];
		document.getElementById(message).innerHTML = "";
	}

	messageInfo.classList.add("hidden");
}

function clearBoard(){
	currentBoard = "---------";

	for (var i = 0; i < 9; i++){
		var row = Math.floor(i / 3) + 1;
		var col = (i % 3) + 1;

		var boxElement = getBox(row, col);
		boxElement.innerHTML = "";
	}
}

function disableButtons(buttons){
	if (buttons === undefined) {
		buttons = gameButtons;
    }

	if (!Array.isArray(buttons)){
		var buttons = [buttons];
	}

	for (var i = 0; i < buttons.length; i++){
		button = buttons[i];
		var buttonElement = document.getElementById(button);
		buttonElement.classList.remove("game-button-hover");
		buttonElement.onclick = null;
		buttonElement.style.cursor = "default";
	}
}

function enableButtons(buttons){
	if (buttons === undefined) {
		buttons = gameButtons;
    }

	if (!Array.isArray(buttons)){
		var buttons = [buttons];
	}

	for (var i = 0; i < buttons.length; i++){
		button = buttons[i];
		var buttonElement = document.getElementById(button);
		buttonElement.classList.add("game-button-hover");
		buttonElement.onclick = buttonFunctions[button];
		buttonElement.style.cursor = "pointer";
	}

	if (document.getElementById("message").innerHTML == resetMessageStart){
		showMessage(resetMessageDone);
	}else if (document.getElementById("message").innerHTML == simMessage){
		if (!stopSim){
			showMessage(simMessageDone);
		}else{
			showMessage(simMessageCancel);
		}
	}
}

function toggleSimButton(){
	var buttonElement = document.getElementById("simulate-button");

	if (buttonElement.innerHTML == "Simulate"){
		buttonElement.innerHTML = "Stop";
		buttonElement.onclick = stopSimulation;
		buttonElement.classList.add("game-button-hover");
		buttonElement.style.cursor = "pointer";
	}else{
		buttonElement.innerHTML = "Simulate";
	}
}

function toggleBatchButton(){
	var buttonElement = document.getElementById("simulate-button");

	if (buttonElement.innerHTML == "Simulate"){
		buttonElement.innerHTML = simMessageBatch;
		buttonElement.classList.add("simulating");
		
	}else{
		buttonElement.classList.remove("simulating");
		buttonElement.innerHTML = "Simulate";
	}
}

function disablePlayer(){
	var board = document.getElementById("board");
	board.onclick = null;
	board.style.cursor = "default";
}

function enablePlayer(){
	var board = document.getElementById("board");
	board.onclick = playerMove;
 	board.style.cursor = "pointer";
}

function showGameInfo(){
	var infoDiv = document.getElementById("game-info");
	infoDiv.style.display = "inline-block";
}

function hideGameInfo(){
	var infoDiv = document.getElementById("game-info");
	infoDiv.style.display = "none";
}

function showProbInfo(){
	var infoDiv = document.getElementById("prob-info");
	infoDiv.style.display = "inline-block";
}

function hideProbInfo(){
	var infoDiv = document.getElementById("prob-info");
	infoDiv.style.display = "none";
}

/////////////////////////////////////////////
//                                         //
//         HTTP Request Functions          //
//                                         //
/////////////////////////////////////////////

function postRequest(url, data, callback){
	if (callback === undefined){
		callback = function(){return;};
	}

	var http = new XMLHttpRequest();
 	http.open("POST", url, true);
 	http.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

 	http.onreadystatechange = function(){
 		if (http.readyState == 4 && http.status == 200){
 			callback(http.responseText);
 		}
 	}

 	http.send(data);
}

function getRequest(url, callback){
	if (callback === undefined){
		callback = function(){return;};
	}

	var http = new XMLHttpRequest();
	http.open("GET", url, true);

	http.onreadystatechange = function(){
		if (http.readyState == 4 && http.status == 200){
			callback();	
		}
	}

	http.send(null);
}

/////////////////////////////////////////////
//                                         //
//            Computer's Move              //
//                                         //
/////////////////////////////////////////////

function updateBoardComputer(board){
	for (var i = 0; i < 9; i++){
		if (board[i] != currentBoard[i]){
			var row = Math.floor(i / 3) + 1;
			var col = (i % 3) + 1;

			var boxElement = getBox(row, col);
			boxElement.innerHTML = compSymbol.toUpperCase();
		}
	}
}

function processComputerMove(response){
	var data = JSON.parse(response);
	updateBoardComputer(data.board);

	if (!data.over){
		var probWin = parseFloat(data.msg);
		showMessage("AI thinks it has a <span>" + toPercent(probWin) + "</span> chance of winning", true);
		enablePlayer();
	}else{
		enableButtons("reset-button");
		showMessage(data.msg);
	}
}

function computerMove(){
	showMessage("AI Is Thinking...");
	postRequest("/next-move", "board=" + currentBoard + "&comp-symbol=" + compSymbol + "&erase=false" + "&simulation=false", processComputerMove);
}

///////////////////////////////////////////////
//                                           //
//               Human's Move                //
//                                           //
///////////////////////////////////////////////

function updateBoardPlayer(){
	var board = "";

	for (var i = 1; i <= 3; i++){
		for (j = 1; j <= 3; j++){
			var boxValue = getBox(i, j).innerHTML.toLowerCase();
			
			if (boxValue == ""){
				boxValue = "-";
			}

			board += boxValue;
		}
	}

	return (board);
}

function processPlayerMove(response){
	var data = JSON.parse(response);
	 		
	if (data.over && !data.tie){
		enableButtons("reset-button");
		showMessage("Human Wins");
		postRequest("/comp-loss", "comp-symbol=" + compSymbol);
	}else if (data.over && data.tie){
		enableButtons("reset-button");
		showMessage("Tie Game");
		postRequest("/comp-tie", "comp-symbol=" + compSymbol);
	}else{
		computerMove();
	}
}

function playerMove(e){
	disablePlayer();

	// Get row and column numbers 
	e.stopPropagation();
	var target = e.target;
	var col = parseInt(target.getAttribute("data-col"));
	var row = parseInt(target.getAttribute("data-row"));
	var boxElement = getBox(row, col);
	
	// Check for valid move
	if (boxElement.innerHTML == ""){
		// Place symbol in box
		boxElement.innerHTML = humanSymbol.toUpperCase();
		currentBoard = updateBoardPlayer();

		// Check if game over
		postRequest("/game-over", "board=" + currentBoard, processPlayerMove);
	}else{
		enablePlayer();
	}
}

/////////////////////////////////////////////
//                                         //
//         Reset Learning History          //
//                                         //
/////////////////////////////////////////////

function resetAI(){
	disableButtons();
	showMessage(resetMessageStart);
	getRequest("/reset-ai", enableButtons);
}

/////////////////////////////////////////////
//                                         //
//    Simulated Game (Computer vs Itself)  //
//                                         //
/////////////////////////////////////////////

function nextSimulatedGame(){
	clearBoard();

	gameNum++;
	simMessage = "Simulating Game " + gameNum;
	showMessage(simMessage);
	
	compSymbol = "x"
	postRequest("/next-move", "board=" + currentBoard + "&comp-symbol=" + compSymbol + "&erase=true" + "&simulation=true", processSimulationMove);
}

function nextSimulatedMove(){
	if (compSymbol == "x"){
		compSymbol = "o";
	}else{
		compSymbol = "x";
	}

	postRequest("/next-move", "board=" + currentBoard + "&comp-symbol=" + compSymbol + "&erase=false" + "&simulation=true", processSimulationMove);	
}

function stopSimulation(){
	stopSim = true;
	disableButtons();
}

function processSimulationMove(response){
	var data = JSON.parse(response);
	updateBoardComputer(data.board);
	currentBoard = data.board;

	if (stopSim){
		enableButtons();
		toggleSimButton();
		clearBoard();
		stopSim = false;
	}else if (!data.over){
		nextSimulatedMove();
	}else if (gameNum < numGames){
		setTimeout(function(){ 
			nextSimulatedGame();
		}, 400);
	}else{
		enableButtons();
		toggleSimButton();
		clearBoard();
	}
}

function processBatchSimulation(response){
	showMessage(simMessageDone);
	enableButtons();
	toggleBatchButton();
}

function batchSimulation(){
	toggleBatchButton();
	postRequest("/batch-sim", "num-games=" + numGames, processBatchSimulation);
}

function startSimulation(){
	numGames = parseInt(document.getElementById("simulate-num").value);
	simMode = document.querySelector("input[name='simulate-mode']:checked").value;
	var errorMessage = "";

	if (simMode == "online"){
		maxGames = maxGamesOnline;
	}else{
		maxGames = maxGamesBatch;
	}

	if (isNaN(numGames)){
		errorMessage = "Invalid Number of Games";
	}else if (numGames <= 0){
		errorMessage = "Number of Games Must Be Positive";
	}else if (numGames > maxGames){
		errorMessage = "Maximum Number of Games Is " + maxGames;
	}
	
	if (errorMessage == ""){
		clearBoard();
		clearMessages();
		disablePlayer();
		disableButtons();	

		if (simMode == "online"){
			gameNum = 0;
			toggleSimButton();
			nextSimulatedGame();
		}else{
			batchSimulation();
		}
	}else{
		showMessage(errorMessage);
	}
}

/////////////////////////////////////////////
//                                         //
//   Interactive Game (Computer vs Human)  //
//                                         //
/////////////////////////////////////////////

function setSymbols(){
	compSymbol = document.querySelector("input[name='comp-move']:checked").value;

	if (compSymbol == "x"){
		humanSymbol = "o";
	}else{
		humanSymbol = "x";
	}
}

function firstMove(){
	if (compSymbol == firstPlayer){
		computerMove();
	}
	else{
		showMessage("Your Move");
		enablePlayer();
	}	
}
function startGame(e){
	disableButtons("reset-button");
	clearMessages();
	clearBoard();
	setSymbols();
	postRequest("/initialize-game", "comp-symbol=" + compSymbol, firstMove);
}

///////////////////////////////////////////////
//                                           //
//            Enable Game Controls           //
//                                           //
///////////////////////////////////////////////

enableButtons();