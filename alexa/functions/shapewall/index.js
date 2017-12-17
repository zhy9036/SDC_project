var emotions = {
    "zero": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "anger": 1,
    "angry": 1,
    "joy": 2,
    "joyful": 2,
    "happy": 2,
    "sadness": 3,
    "sad": 3,
    "fear": 4,
    "fearful": 4,
    "scared": 4,
    "afraid": 4,
    "surprise": 5,
    "surprised": 5,
    "disgust": 6,
    "disgusted": 6
};

var http = require('http');
var querystring = require('querystring');
var urlString = "";
var output = 1;
var newConfig = 1;
// Route the incoming request based on type (LaunchRequest, IntentRequest,
// etc.) The JSON body of the request is provided in the event parameter.


/**
 * Called when the session starts.
 */
function onSessionStarted(sessionStartedRequest, session) {
    // add any session init logic here
}

/**
 * Called when the user invokes the skill without specifying what they want.
 */
function onLaunch(launchRequest, session, callback) {
    getWelcomeResponse(callback);
}

/**
 * Called when the user specifies an intent for this skill.
 */
function onIntent(intentRequest, session, callback) {

    var intent = intentRequest.intent;
    var intentName = intentRequest.intent.name;
    var output = "Welcome to Shape Wall! How are you feeling?";
    // var output = "Welcome to Shape Wall! Select a configuration.";
    var sessionAttributes = {
        "speechOutput": output,
        "repromptText": output
    };
    
    console.log(intentName);
    if (intentName == "emotionPresetIntent") {
        handleEmotionPresetResponse(intent, session, callback);
    }
    else if (intentName == "exitIntent") {
        callback(sessionAttributes, buildSpeechletResponseWithoutCard( "Exiting Shape Wall", "", true));
    }
    else {
        callback(sessionAttributes, buildSpeechletResponseWithoutCard( "Invalid Command. Try Again", "", false));
    }
}

/**
 * Called when the user ends the session.
 * Is not called when the skill returns shouldEndSession=true.
 */
function onSessionEnded(sessionEndedRequest, session) {

}

// ------- Skill specific logic -------

function getWelcomeResponse(callback) {
    var output = "Welcome to Shape Wall! Select a configuration.";

    var shouldEndSession = false;

    var header = "S.H.A.P.E. Wall!";

    var sessionAttributes = {
        "speechOutput": output,
        "repromptText": output
    };
    callback(sessionAttributes, buildSpeechletResponse(header, output, output, shouldEndSession));
}

function handleEmotionPresetResponse(intent, session, callback) {
    if (intent.slots.emotion.value === null) {
        callback(session.attributes, buildSpeechletResponseWithoutCard(speechOutput, "Configuration not recognized. Please try again.", false));
        return;
    }
    var emotion = intent.slots.emotion.value.toLowerCase();
    console.log(emotion);
    
    // Select return value based on given emotion/integer
    switch (emotion) {
        case "0":
            newConfig = 0;
            break;
        case "anger":
        case "angry":
        case "1":
            newConfig = 1;
            break;
        case "joy":
        case "joyful":
        case "happy":
        case "2":
            newConfig = 2;
            break;
        case "sadness":
        case "sad":
        case "3":
            newConfig = 3;
            break;
        case "fear":
        case "fearful":
        case "scared":
        case "afraid":
        case "4":
            newConfig = 4;
            break;
        case "surprise":
        case "surprised":
        case "5":
            newConfig = 5;
            break;
        case "disgust":
        case "disgusted":
        case "6":
            newConfig = 6;
            break;
    }
    
    console.log(newConfig)
    urlString = "/previewData.php?value=" + newConfig;
    console.log(urlString);
    var speechOutput = "We have an error";

    putData(function (callback2) {
        var speechOutput = "We have an error";
        if (callback2 != "ERROR") {
            console.log("resultofGet: " + callback2);
            speechOutput = "The wall has been updated. Ready for next command.";
        }
        callback(session.attributes, buildSpeechletResponseWithoutCard(speechOutput, "Please say another command.", false));
    });
}

function putData(callback) {
    var options = {
      hostname: 'yangzhang7.pythonanywhere.com',
      port: '80',
      path: '/currentWall/',
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
      }
    };
    
    var wall = {
        "currentWall" : newConfig,
        "deviceID" : 0
    }
    
    var req = http.request(options, function (res) {
        
        if (res) {
            callback(res.statusCode);
        } else {
            callback("ERROR");
        }
    });
    
    console.log(options.path);
    req.write(JSON.stringify(wall));
    req.end();
}

function submitData(callback) {

    http.get('http://shapetest.loganstrong.com/Updater.php', function (res) {
        if (res) {
            callback(res.statusCode);
        } else {
            callback("ERROR");
        }
    });
}

function handleGetHelpRequest(intent, session, callback) {
    // Ensure that session.attributes has been initialized
    if (!session.attributes) {
        session.attributes = {};
    }
}

function handleFinishSessionRequest(intent, session, callback) {
    // End the session with a "Good bye!" if the user wants to quit the game
    callback(session.attributes,
        buildSpeechletResponseWithoutCard("Good bye!", "", true));
}


// ------- Helper functions to build responses for Alexa -------


function buildSpeechletResponse(title, output, repromptText, shouldEndSession) {
    return {
        outputSpeech: {
            type: "PlainText",
            text: output
        },
        card: {
            type: "Simple",
            title: title,
            content: output
        },
        reprompt: {
            outputSpeech: {
                type: "PlainText",
                text: repromptText
            }
        },
        shouldEndSession: shouldEndSession
    };
}

function buildSpeechletResponseWithoutCard(output, repromptText, shouldEndSession) {
    return {
        outputSpeech: {
            type: "PlainText",
            text: output
        },
        reprompt: {
            outputSpeech: {
                type: "PlainText",
                text: repromptText
            }
        },
        shouldEndSession: shouldEndSession
    };
}

function buildResponse(sessionAttributes, speechletResponse) {
    return {
        version: "1.0",
        sessionAttributes: sessionAttributes,
        response: speechletResponse
    };
}

exports.handle = function(event, context) {
    try {
        //console.log("event.session.application.applicationId=" + event.session.application.applicationId);

        /**
         * Uncomment this if statement and populate with your skill's application ID to
         * prevent someone else from configuring a skill that sends requests to this function.
         */

        // if (event.session.application.applicationId !== "arn:aws:lambda:us-east-1:990858326956:function:shapeWall") {
        //     context.fail("Invalid Application ID");
        //  }

        if (event.session.new) {
            onSessionStarted({requestId: event.request.requestId}, event.session);
        }

        if (event.request.type === "LaunchRequest") {
            onLaunch(event.request,
                event.session,
                function callback(sessionAttributes, speechletResponse) {
                    context.succeed(buildResponse(sessionAttributes, speechletResponse));
                });
        } else if (event.request.type === "IntentRequest") {
            onIntent(event.request,
                event.session,
                function callback(sessionAttributes, speechletResponse) {
                    context.succeed(buildResponse(sessionAttributes, speechletResponse));
                });
        } else if (event.request.type === "SessionEndedRequest") {
            onSessionEnded(event.request, event.session);
            context.succeed();
        }
    } catch (e) {
        context.fail("Exception: " + e);
    }
}

