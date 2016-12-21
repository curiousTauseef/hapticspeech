/*
 _   _             _   _        _____                      _     
| | | |           | | (_)      /  ___|                    | |    
| |_| | __ _ _ __ | |_ _  ___  \ `--. _ __   ___  ___  ___| |__  
|  _  |/ _` | '_ \| __| |/ __|  `--. \ '_ \ / _ \/ _ \/ __| '_ \ 
| | | | (_| | |_) | |_| | (__  /\__/ / |_) |  __/  __/ (__| | | |
\_| |_/\__,_| .__/ \__|_|\___| \____/| .__/ \___|\___|\___|_| |_|
            | |                      | |                         
            |_|                      |_|                         

*/


//-----------------------------------------------------------------------
// imports
//-----------------------------------------------------------------------

import processing.sound.*;
import processing.serial.*;

//-----------------------------------------------------------------------
// globals
//-----------------------------------------------------------------------

SoundFile input;
Amplitude rms;
SinOsc sine;

//settings for sine wave generator
float freq=400;
float amp=0.5;
float pos;
float scaleFactor = 2;

//settings for RMS amp analysis
int scale=1;
float smoothRMS = 0;
float maxRMS = 0;
float smoothFactor = 0.4; //must be between 0-1

//for filesystem access
int fileIndex = 0;
String path = sketchPath();
String[] filenames;


//-----------------------------------------------------------------------
// functions
//-----------------------------------------------------------------------

// This function returns all the files in a directory as an array of Strings  
String[] listFileNames(String dir) {
  File file = new File(dir);
  if (file.isDirectory()) {
    String names[] = file.list();
    return names;
  } else {
    // If it's not a directory
    return null;
  }
}


//-----------------------------------------------------------------------
// setup
//-----------------------------------------------------------------------
void setup() {
    size(640,360);
    background(255);
        
    //gets list of all filenames in `data`, for some reason we can only
    //run this in setup.
    String[] filenames = listFileNames(sketchPath()+"/data/");
    pushNames(filenames);
    
    printArray(filenames);
    
    //_______________
    // audio input   \
    //-------------------------------------------------------------------
    
    //create a new audio file using the file directory.
    //must be a mono wav file at 44.1kHz
    input = new SoundFile(this, filenames[fileIndex]);
    
    // plays wav file
    input.play();
    
    // create a new Amplitude analyzer
    rms = new Amplitude(this);
    
    // Patch the input to an volume analyzer
    rms.input(input);
    
    
    //__________________
    // sine generator   \
    //-------------------------------------------------------------------
    
    // Create and start the sine oscillator.
    sine = new SinOsc(this);
    
    //Start the Sine Oscillator. 
    sine.play();
    

}     

//-----------------------------------------------------------------------
// draw loop
//-----------------------------------------------------------------------
void draw() {
  
    input.pan(-1);
    sine.pan(1);
    background(60,60,60);
    
    
    // adjust the volume of the audio input
    input.amp(2.0);
    
    //smooth input values
    smoothRMS = smoothFactor * smoothRMS + (1-smoothFactor) * rms.analyze();
    text("smoothRMS: "+rms.analyze(),20,20);
    text("current file: "+filenames[fileIndex],20,40);
    if (rms.analyze()>1){
      println("YUP");
    }
    
    // rms.analyze() return a value between 0 and 1. To adjust
    // the scaling and mapping of an ellipse we scale from 0 to 0.5
    scale=int(map(smoothRMS, 0, 0.5, 1, 350));
    noStroke();
    
    //amplitude and frequency are coupled to smoothRMS
    sine.amp(smoothRMS*scaleFactor);
    //sine.freq(smoothRMS*1000);
    
    fill(255,0,100);
    // We draw an ellispe coupled to the audio analysis
    ellipse(width/2, height/2, 1*scale, 1*scale); 
}


void keyPressed(){
  //load up next file
  if(key=='d' || key=='D'){
        fileIndex++;
        fill(255,255,255);
        input.stop();
        input = new SoundFile(this, filenames[fileIndex]);
        input.play();
        rms.input(input);
      }
}

void pushNames(String[] nameArray){
  filenames = nameArray;
}