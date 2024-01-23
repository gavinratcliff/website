function main() {
	const canvas = document.getElementById("glcanvas");
	
	const gl = canvas.getContext("webgl");
	if (gl == null) {
		alert('cannot initialize webgl');
		return;
	}
	
	const indexBuffer = initIndexBuffer(gl);

	gl.clearColor(1.0, 1.0, 1.0, 1.0);
	gl.clear(gl.COLOR_BUFFER_BIT);
}

//main();
