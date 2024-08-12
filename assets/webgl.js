const vsSource = `
    attribute vec4 aVertexPosition;

    uniform mat4 uModelViewMatrix;
    uniform mat4 uProjectionMatrix;

    void main(void) {
      gl_Position = uProjectionMatrix * uModelViewMatrix * aVertexPosition;
    }
`;

const fsSource = `
    void main(void) {
      gl_FragColor = vec4(0.0, 0.0, 0.0, 1.0);
    }
`;

let cubeRotation = 0;
let deltaTime = 0;

function initPositionBuffer(gl, n) {
    let positions = [];
    let indices = [];

    if (n === 4) {
        // Tetrahedron
        positions = [
            1, 1, 1,
            -1, -1, 1,
            -1, 1, -1,
            1, -1, -1,
        ];

        indices = [
            0, 1, 2,
            1, 2, 3,
            2, 3, 0,
            3, 0, 1,
        ];

    } else if (n === 6) {
        // Cube
        positions = [
            -1, -1, -1,
            1, -1, -1,
            1, 1, -1,
            -1, 1, -1,
            -1, -1, 1,
            1, -1, 1,
            1, 1, 1,
            -1, 1, 1,
        ];

        indices = [
            0, 1, 2, 0, 2, 3, // Front
            4, 5, 6, 4, 6, 7, // Back
            0, 1, 5, 0, 5, 4, // Bottom
            2, 3, 7, 2, 7, 6, // Top
            0, 3, 7, 0, 7, 4, // Left
            1, 2, 6, 1, 6, 5  // Right
        ];

    } else if (n === 8) {
        // Octahedron
        positions = [
            1, 0, 0,
            -1, 0, 0,
            0, 1, 0,
            0, -1, 0,
            0, 0, 1,
            0, 0, -1,
        ];

        indices = [
            0, 2, 4,
            0, 3, 4,
            1, 2, 4,
            1, 3, 4,
            0, 2, 5,
            0, 3, 5,
            1, 2, 5,
            1, 3, 5,
        ];

    } else if (n === 12) {
        // Dodecahedron (approximation)
        const phi = (1 + Math.sqrt(5)) / 2; // Golden ratio
        positions = [
            // Vertices of a dodecahedron
            1, 1, 1,
            1, 1, -1,
            1, -1, 1,
            1, -1, -1,
            -1, 1, 1,
            -1, 1, -1,
            -1, -1, 1,
            -1, -1, -1,
            0, 1/phi, phi,
            0, 1/phi, -phi,
            0, -1/phi, phi,
            0, -1/phi, -phi,
            1/phi, phi, 0,
            1/phi, -phi, 0,
            -1/phi, phi, 0,
            -1/phi, -phi, 0,
            phi, 0, 1/phi,
            phi, 0, -1/phi,
            -phi, 0, 1/phi,
            -phi, 0, -1/phi,
        ];

        indices = [
            0, 8, 4,
            0, 16, 8,
            0, 12, 16,
            1, 17, 9,
            1, 13, 17,
            1, 12, 13,
            2, 10, 6,
            2, 16, 10,
            2, 13, 16,
            3, 11, 7,
            3, 17, 11,
            3, 13, 17,
            4, 14, 5,
            4, 18, 14,
            4, 8, 18,
            5, 15, 7,
            5, 19, 15,
            5, 14, 19,
            6, 18, 8,
            6, 10, 18,
            6, 19, 10,
            7, 15, 11,
            7, 19, 15,
            7, 19, 15,
        ];

    } else if (n === 20) {
        // Icosahedron
        const phi = (1 + Math.sqrt(5)) / 2; // Golden ratio
        positions = [
            -1, phi, 0,
            1, phi, 0,
            -1, -phi, 0,
            1, -phi, 0,
            0, -1, phi,
            0, 1, phi,
            0, -1, -phi,
            0, 1, -phi,
            phi, 0, -1,
            phi, 0, 1,
            -phi, 0, -1,
            -phi, 0, 1,
        ];

        indices = [
            0, 11, 5,
            0, 5, 1,
            0, 1, 7,
            0, 7, 10,
            0, 10, 11,
            1, 5, 9,
            5, 11, 4,
            11, 10, 2,
            10, 7, 6,
            7, 1, 8,
            3, 9, 4,
            3, 4, 2,
            3, 2, 6,
            3, 6, 8,
            3, 8, 9,
            4, 9, 5,
            2, 4, 11,
            6, 2, 10,
            8, 6, 7,
            9, 8, 1,
        ];
    } else {
        alert("n value not supported. Please use n=4, 6, 8, 12, or 20.");
        return null;
    }

    const positionBuffer = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, positionBuffer);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(positions), gl.STATIC_DRAW);

    const indexBuffer = gl.createBuffer();
    gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, indexBuffer);
    gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, new Uint16Array(indices), gl.STATIC_DRAW);

    return { position: positionBuffer, indices: indexBuffer, vertexCount: indices.length };
}

function initShaderProgram(gl, vsSource, fsSource) {
    const vertexShader = loadShader(gl, gl.VERTEX_SHADER, vsSource);
    const fragmentShader = loadShader(gl, gl.FRAGMENT_SHADER, fsSource);

    const shaderProgram = gl.createProgram();
    gl.attachShader(shaderProgram, vertexShader);
    gl.attachShader(shaderProgram, fragmentShader);
    gl.linkProgram(shaderProgram);

    if (!gl.getProgramParameter(shaderProgram, gl.LINK_STATUS)) {
        alert('Unable to initialize the shader program: ' + gl.getProgramInfoLog(shaderProgram));
        return null;
    }

    return shaderProgram;
}

function loadShader(gl, type, source) {
    const shader = gl.createShader(type);
    gl.shaderSource(shader, source);
    gl.compileShader(shader);

    if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
        alert('An error occurred compiling the shaders: ' + gl.getShaderInfoLog(shader));
        gl.deleteShader(shader);
        return null;
    }

    return shader;
}

function drawScene(gl, programInfo, buffers, rotation) {
    gl.clearColor(1.0, 1.0, 1.0, 1.0);
    gl.clearDepth(1.0);
    gl.enable(gl.DEPTH_TEST);
    gl.depthFunc(gl.LEQUAL);

    gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);

    const fieldOfView = 45 * Math.PI / 180;
    const aspect = gl.canvas.clientWidth / gl.canvas.clientHeight;
    const zNear = 0.1;
    const zFar = 100.0;
    const projectionMatrix = mat4.create();

    mat4.perspective(projectionMatrix, fieldOfView, aspect, zNear, zFar);

    const modelViewMatrix = mat4.create();
    mat4.translate(modelViewMatrix, modelViewMatrix, [-0.0, 0.0, -6.0]);
    mat4.rotate(modelViewMatrix, modelViewMatrix, rotation, [0, 0, 1]);
    mat4.rotate(modelViewMatrix, modelViewMatrix, rotation * 0.7, [0, 1, 0]);

    {
        const numComponents = 3;
        const type = gl.FLOAT;
        const normalize = false;
        const stride = 0;
        const offset = 0;
        gl.bindBuffer(gl.ARRAY_BUFFER, buffers.position);
        gl.vertexAttribPointer(
            programInfo.attribLocations.vertexPosition,
            numComponents,
            type,
            normalize,
            stride,
            offset);
        gl.enableVertexAttribArray(programInfo.attribLocations.vertexPosition);
    }

    gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, buffers.indices);

    gl.useProgram(programInfo.program);

    gl.uniformMatrix4fv(
        programInfo.uniformLocations.projectionMatrix,
        false,
        projectionMatrix);
    gl.uniformMatrix4fv(
        programInfo.uniformLocations.modelViewMatrix,
        false,
        modelViewMatrix);

    const vertexCount = buffers.vertexCount;
    const type = gl.UNSIGNED_SHORT;
    const offset = 0;
    gl.drawElements(gl.LINES, vertexCount, type, offset);
}

function initBuffers(gl, n) {
    return initPositionBuffer(gl, n);
}

document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.querySelector('#glcanvas');
    const gl = canvas.getContext('webgl');

    if (!gl) {
        alert('Unable to initialize WebGL. Your browser may not support it.');
        return;
    }

    const shaderProgram = initShaderProgram(gl, vsSource, fsSource);

    const programInfo = {
        program: shaderProgram,
        attribLocations: {
            vertexPosition: gl.getAttribLocation(shaderProgram, 'aVertexPosition'),
        },
        uniformLocations: {
            projectionMatrix: gl.getUniformLocation(shaderProgram, 'uProjectionMatrix'),
            modelViewMatrix: gl.getUniformLocation(shaderProgram, 'uModelViewMatrix'),
        },
    };

    var n = 0;
    const randomInt = Math.floor(Math.random() * 5);
    if (randomInt == 0) {
      n = 4;
    }
    if (randomInt == 1) {
      n = 6;
    }
    if (randomInt == 2) {
      n = 8;
    }
    if (randomInt == 3) {
      n = 12;
    }
    if (randomInt == 4) {
      n = 20;
    }

    const buffers = initBuffers(gl, n);

    let then = 0;

    function render(now) {
        now *= 0.001;
        const deltaTime = now - then;
        then = now;

        cubeRotation += deltaTime;

        drawScene(gl, programInfo, buffers, cubeRotation);

        requestAnimationFrame(render);
    }
    requestAnimationFrame(render);
});
