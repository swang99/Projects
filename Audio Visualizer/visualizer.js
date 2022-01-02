var song, amplitude;
var song_num = 0;
var img;
var fft;
var particles = [];
const MIN_RADIUS = 150;
const MAX_RADIUS = 350;

/* playlist */
var tracks = new Map();
tracks.set('0', ['BrokenHeart.m4a', 'Me and My Broken Heart', 'Rixton']);
tracks.set('1', ['UsVsWorld.m4a', 'Us Against the World', 'Darren Styles']);
tracks.set('2', ['StereoHearts.m4a', 'Stereo Hearts', 'Gym Class Heroes']);
tracks.set('3', ['FireflyII.m4a', 'Firefly, Part II', 'Jim Yosef']);
tracks.set('4', ['Lily.m4a', 'Lily', 'Alan Walker'])

/* setup and waveform */
function preload() {
  song = loadSound(tracks.get(str(song_num))[0]);
	song.rate(1.05);
	song.setVolume(0.75);
	img = loadImage('back1.jpeg');
}

function setup() {
	// canvas drawing tools
  let cnv = createCanvas(windowWidth, windowHeight - 75);
	cnv.mousePressed(playPauseBtn);
	
	angleMode(DEGREES); 
	frameRate(50);
	rectMode(CENTER);

	// audio analysis tools
	fft = new p5.FFT();
	amplitude = new p5.Amplitude();
}

// dynamic resizing based on window
function windowResized() {
	resizeCanvas(windowWidth, windowHeight);
}

/* drawing loop */
function draw() {
	background(img);
	stroke(255); // outline color of visualizer
	translate(width/2, height/2) // center visualizer
	fill('rgba(20,20,20,0.6)')
	rect(0, 0, width, height);
	noStroke();
	ellipse(0, 0, MIN_RADIUS + MAX_RADIUS);

	trackDetails();

	// update song progress bar and time
	if (song.isPlaying() && frameCount % 30 == 0) {
		updateBar(int(song.currentTime()));
		updateTime(int(song.currentTime()));
		updateTimeRem(int(song.currentTime()));
		if (abs(song.duration() - song.currentTime()) < 0.5) {
			shuffleLoop();
		}
	}

	// waveform analysis on time domain
	let wave = fft.waveform();
	
	// create two halves of visualizer circle
	noFill();
	let vis_col = soundColor();
	stroke(vis_col[0],vis_col[1],vis_col[2])
	
	for (let h = -1; h <= 1; h += 2) {
		beginShape();
		for (let i = 0; i <= 180; i += 0.75) {
			let index = floor(map(i, 0, 180, 0, wave.length - 1))
			let r = map(wave[index], -1, 1, MIN_RADIUS, MAX_RADIUS)
			let x = r * h * sin(i);
			let y = r * cos(i);
			vertex(x,y);
		}
		endShape();
	}
	
	// generate particles
	if (song.isPlaying()) {
		for (let i = 0; i < 3; i++) {
			particles.push(new Particle());
		}
	}

	// particle velocity and color depends on wave amplitude
	for (let i = 0; i < particles.length; i++) {
		if (!particles[i].onEdge()) {
			particles[i].update(amplitude.getLevel()); 
			particles[i].show(vis_col[0],vis_col[1],vis_col[2]);
		} else {
			// remove off-screen particles
			particles.splice(i, 1); 
		}
	}
}

function trackDetails() {
	textFont('Lato');
	
	// name
	textSize(25);
	textStyle(BOLD);
	textAlign(CENTER);
	fill(255);
	text(tracks.get(str(song_num))[1], 0, 0);

	// artist
	textSize(20);
	textStyle(NORMAL);
	text(tracks.get(str(song_num))[2], 0, 30);
}

function soundColor() {
	let color = [255,255,255];
	if (amplitude.getLevel() >= 0.4) {
		color = [255,50,0];
	} else if (amplitude.getLevel() >= 0.3) {
		color = [255,165,0];
	}
	return color;
}

/* music player controls */
// previous song button
function prevSong() {
	if (song_num == 0) {
		song_num = tracks.size - 1;
	} else {
		song_num--;
	}

	song.stop();
	song = loadSound(tracks.get(str(song_num))[0], playPauseBtn);
}

// play/pause button
function playPauseBtn() {
	icon = document.getElementById('play-pause');
	if (song.isPlaying()) {
		icon.setAttribute('name', 'play');
		song.pause();
		noLoop();
	} else {
		icon.setAttribute('name', 'pause');
		song.play();
		loop();
	}
}

// next song button
function nextSong() {
	if (song_num == tracks.size - 1) {
		song_num = 0;
	} else {
		song_num++;
	}

	song.stop();
	song = loadSound(tracks.get(str(song_num))[0], playPauseBtn);
}

// shuffle/loop button
function toggleShuffleLoop(icon) {
	if (icon.getAttribute('name') == 'shuffle') {
		icon.setAttribute('name', 'repeat');
	} else {
		icon.setAttribute('name', 'shuffle');
	}
}

function shuffleLoop() {
	let button_mode = document.getElementById('shuffle-loop').name;
	let finished = song.duration() - song.currentTime() < 0.5; 

	if (finished && button_mode == 'shuffle') {
		let rand_num = int(random(0, tracks.size));
		while (rand_num == song_num) {
			rand_num = int(random(0, tracks.size));
		}
		song.stop();
		song_num = rand_num;
		console.log(song_num);
		song = loadSound(tracks.get(str(song_num))[0], playPauseBtn);
	} 
	
	else if (finished && button_mode == 'repeat') {
		song.loop();
	}
}

// upload song button
function uploadSong() {
	let uploaded_files = document.getElementById('file-input').files;
	for (let i = 0; i < uploaded_files.length; i++) {
		let song_file = uploaded_files[i].name;
		let song_name = prompt("Successfully uploaded " + song_file + ". Enter the name of the song: ");
		let song_artist = prompt("Enter the name of the artist: ");
		tracks.set(str(tracks.size), [song_file, song_name, song_artist]);
	}
}

/* progress bar */
// update progress bar and time
function updateBar(curr_time) {
	let bar = document.getElementById('time-bar');
	let width = (curr_time / song.duration()) * 100;
	bar.style.width = width + 'vw';
}

function updateTime(curr_time) {
	let time = document.getElementById('time-text');
	let minutes = Math.floor(int(curr_time) / 60);
	let secs = int(curr_time - (60 * minutes));

	if (secs < 10) {
		time.innerHTML = str(minutes) + ":0" + str(secs);
	} else {
		time.innerHTML = str(minutes) + ":" + str(secs);
	}
}

function updateTimeRem(curr_time) {
	let time_rem = document.getElementById('time-text-rem');
	let minutes = Math.floor((int(song.duration()) - curr_time) / 60);
	let secs = int(song.duration() - ((60 * minutes) + curr_time));

	if (secs < 10) {
		time_rem.innerHTML = "-" + str(minutes) + ":0" + str(secs);
	} else {
		time_rem.innerHTML = "-" + str(minutes) + ":" + str(secs);
	}
}

function jumpProgress() {
	song.clearCues();
	let bar = document.getElementById('time-bar');
	let width = (mouseX / windowWidth) * 100;
	let new_time = song.duration() * (width / 100);
	
	bar.style.width = width + 'vw';
	updateTime(new_time);

	if (song.isPlaying()) {
		song.jump(new_time);
	} else {
		song.addCue(song.currentTime() + 1e-5, jumpOnPause, new_time)
	}

	function jumpOnPause() {
		song.clearCues();
		song.jump(new_time);
	}
}

/* particles */
class Particle {
	constructor() {
		this.pos = p5.Vector.random2D().mult((MIN_RADIUS + MAX_RADIUS) / 2);
		this.velocity = createVector(0, 0)
		this.accel = this.pos.copy().mult(random(0.0002, 0.002))

		this.w = 20 * amplitude.getLevel();
	}

	update(amp) {
		for (let i = 0; i < ceil(amp * 10); i++) {
			this.pos.add(this.velocity);
		}
		this.velocity.add(this.accel);
	}

	show(r,g,b) {
		noStroke();
		fill(r,g,b);
		ellipse(this.pos.x, this.pos.y, this.w);
	}

	onEdge() {
		return this.pos.x < -width / 2 || this.pos.x > width / 2 || this.pos.y < -height / 2 || this.pos.y > height / 2;
	}
}

// potential extensions
// predicting a bass drop
// time bar