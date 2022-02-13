let song, amplitude, img, fft;
let song_num = 0;
let particles = [];
let window_width, window_height;
let min_radius, max_radius; // 150, 350
const FRAME_RATE = 30;

/* playlist */
let tracks = new Map();
tracks.set('0', ['media/Orange7.m4a', 'Orange', 'オレンジ']);
tracks.set('6', ['media/BrokenHeart.m4a', 'Me and My Broken Heart', 'Rixton']);
tracks.set('2', ['media/UsVsWorld.m4a', 'Us Against the World', 'Darren Styles']);
tracks.set('4', ['media/StereoHearts.m4a', 'Stereo Hearts', 'Gym Class Heroes']);
tracks.set('3', ['media/FireflyII.m4a', 'Firefly, Part II', 'Jim Yosef']);
tracks.set('5', ['media/Lily.m4a', 'Lily', 'Alan Walker'])
tracks.set('1', ['media/VioletsLetter.m4a', 'Violet\'s Letter', 'Evan Call'])

/* setup and waveform */
function preload() {
  song = loadSound(tracks.get(str(song_num))[0]);
}

function setup() {
	// create canvas, determine size of audio visualizer
	img = createImg('https://i3.ytimg.com/vi/wdRCSZBvJHc/maxresdefault.jpg', 'Major Gilbert')
	img.position(0, -10000);

  let cnv = createCanvas(windowWidth, windowHeight);
	cnv.mousePressed(playPauseBtn);
	resizeCircle();
	angleMode(DEGREES); 
	frameRate(FRAME_RATE);
	rectMode(CENTER);

	// audio analysis tools
	fft = new p5.FFT();
	amplitude = new p5.Amplitude();
}

// dynamic resizing based on window
function windowResized() {
	resizeCanvas(windowWidth, windowHeight);
	resizeCircle();
}

function resizeCircle() {
	window_width = windowWidth;
	window_height = windowHeight;
	min_radius = 20 * (window_height/window_width);
	max_radius = 300;
}

/* drawing loop */
function draw() {
	drawCanvas();
	trackDetails();
	createVisualizer();

	// update song progress bar and time
	if (song.isPlaying() && frameCount % (FRAME_RATE/4) == 0) {
		updateBar(int(song.currentTime()));
		updateTime(int(song.currentTime()));
		updateTimeRem(int(song.currentTime()));
		if (song.currentTime() > Math.floor(song.duration())) {
			shuffleLoop();
		}
	}
	
	function drawCanvas() {
		background(220);
		image(img, 0, 0);
		stroke(255); // outline color of visualizer
		translate(width/2, height/2) // center visualizer
		fill(`rgba(20,20,20,${Math.max(amplitude.getLevel(), 0.3)})`)
		rect(0, 0, width, height);
		noStroke();
		ellipse(0, 0, min_radius + max_radius);
	}
	
	function trackDetails() {
		// name
		textFont('Lato');
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

	function createVisualizer() {
		let wave = fft.waveform(); // waveform analysis on time domain
		min_radius = 400 * amplitude.getLevel() * (window_height/window_width);
		
		noFill();
		let vis_col = soundColor();
		stroke(220);
		//stroke(vis_col[0],vis_col[1],vis_col[2])
		
		for (let h = -1; h <= 1; h += 2) {
			beginShape();
			for (let i = 0; i <= 180; i += 0.75) {
				let index = floor(map(i, 0, 180, 0, wave.length - 1))
				let r = map(wave[index], -1, 1, min_radius, max_radius*0.75)
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
	
	function soundColor() {
		let color = [255,255,255];
		if (amplitude.getLevel() >= 0.4) {
			color = [255,50,0];
		} else if (amplitude.getLevel() >= 0.3) {
			color = [255,165,0];
		}
		return color;
	}

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
	let finished = song.currentTime() > Math.floor(song.duration());

	if (finished && button_mode == 'shuffle') {
		let rand_num = int(random(0, tracks.size));
		while (rand_num == song_num) {
			rand_num = int(random(0, tracks.size));
		}
		
		song_num = rand_num;
		song.playMode('restart');
		song = loadSound(tracks.get(str(song_num))[0], playPauseBtn);
		
	} 
	
	else if (finished && button_mode == 'repeat') {
		song.playMode('restart');
		song.loop();
	}
}

// upload song button
function uploadSong() {
	let uploaded_files = document.getElementById('file-input').files;
	for (let i = 0; i < uploaded_files.length; i++) {
		let song_file = "media/" + uploaded_files[i].name;
		let song_name = prompt("Successfully uploaded " + song_file + ". Enter the name of the song: ");
		let song_artist = prompt("Enter the name of the artist: ");
		tracks.set(str(tracks.size), [song_file, song_name, song_artist]);
		console.log(tracks)
	}
}

// upload url button
function uploadURL() {
	let yt_url = prompt("Enter the URL of a Youtube video: ");
	if (yt_url != null) {
		let video_info = `https://www.youtube.com/oembed?url=${yt_url}&format=json`
		fetch(video_info)
			.then(response => response.json())
			.then(function(data) {
				let n = data["thumbnail_url"].lastIndexOf('/');
				let thumbnail_url = data["thumbnail_url"].substring(0, n+1) + 'maxresdefault.jpg';
				setThumbnail(thumbnail_url)
			})
			.catch(console.error('Video does not exist'));
		
		function setThumbnail(thumb) {
			img = createImg(thumb, '');
			img.position(0, -10000);
		}
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
		this.pos = p5.Vector.random2D().mult((min_radius + max_radius) / 2);
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
// insert audio based on youtube url