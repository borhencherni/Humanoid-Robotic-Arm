let video;
let handPoseModel, bodyPoseModel;
let hands = [];
let poses = [];
let skeletonConnections = [];

// Load both models in preload
function preload() {
  handPoseModel = ml5.handPose();
  bodyPoseModel = ml5.bodyPose();
}

function setup() {
  createCanvas(640, 480);

  video = createCapture(VIDEO);
  video.size(640, 480);
  video.hide();

  handPoseModel.detectStart(video, gotHands);
  bodyPoseModel.detectStart(video, gotPoses);
  skeletonConnections = bodyPoseModel.getSkeleton();
}

function draw() {
  image(video, 0, 0, width, height);

  drawHandLandmarks();
  drawBodySkeleton();

  // Add gesture detection logic here
  if (hands.length > 0) {
    const hand = hands[0]; // Use the first detected hand
    const landmarks = hand.keypoints;

    const indexTip = getPoint(landmarks, "index_finger_tip");
    const middleTip = getPoint(landmarks, "middle_finger_tip");
    const wrist = getPoint(landmarks, "wrist");

    if (indexTip && middleTip && wrist) {
      const avgTipY = (indexTip.y + middleTip.y) / 2;

      if (avgTipY < wrist.y - 40) {
        console.log("✋ Gesture Detected: Open Hand");
        sendCommand("open");
      } else if (avgTipY > wrist.y - 10) {
        console.log("✊ Gesture Detected: Fist");
        sendCommand("close");
      }
    }
  }
}

function drawHandLandmarks() {
  for (let i = 0; i < hands.length; i++) {
    const hand = hands[i];
    for (let j = 0; j < hand.keypoints.length; j++) {
      const kp = hand.keypoints[j];
      fill(0, 255, 0);
      noStroke();
      circle(kp.x, kp.y, 10);
    }
  }
}

function drawBodySkeleton() {
  for (let i = 0; i < poses.length; i++) {
    const pose = poses[i];

    for (let j = 0; j < skeletonConnections.length; j++) {
      const [a, b] = skeletonConnections[j];
      const pointA = pose.keypoints[a];
      const pointB = pose.keypoints[b];

      if (pointA.confidence > 0.1 && pointB.confidence > 0.1) {
        stroke(255, 0, 0);
        strokeWeight(2);
        line(pointA.x, pointA.y, pointB.x, pointB.y);
      }
    }

    for (let k = 0; k < pose.keypoints.length; k++) {
      const kp = pose.keypoints[k];
      if (kp.confidence > 0.1) {
        fill(0, 255, 0);
        noStroke();
        circle(kp.x, kp.y, 10);
      }
    }
  }
}

// Callback for handpose
function gotHands(results) {
  hands = results;
}

// Callback for bodypose
function gotPoses(results) {
  poses = results;
}

// Utility: Get landmark point by name
function getPoint(landmarks, name) {
  return landmarks.find(kp => kp.name === name);
}

// Placeholder for command sending
function sendCommand(command) {
  // Replace with WebSocket or MQTT logic
  console.log("Send command:", command);
}
