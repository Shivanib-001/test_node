const express = require("express");
const fs = require("fs");
const path = require("path");

const app = express();
app.use(express.json());

let gcp = [];


class GNSSData {
    constructor(filePath) {
        this.path = filePath; 
    }

    last_data() {
        try {
           
            const rawData = fs.readFileSync(this.path, "utf-8");

            const lines = rawData.trim().split('\n');

            const lastLine = lines[lines.length - 1];

            const obj = JSON.parse(lastLine);
            
            return obj; 
        } catch (e) {
            console.error("Error reading or parsing last line:", e.message);
            return null;
        }
    }
}



class Run_process {
    stopobject() {
        return "stopped";
    }
}

const data_read = new GNSSData("../data/gnss.jsonl");
const proc = new Run_process();

app.get("/livelocation", (req, res) => {
    res.set({
        "Content-Type": "text/event-stream",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive"
    });

    const logfile = fs.createWriteStream("../data/live_log.txt", { flags: "a" });

    const interval = setInterval(() => {
        try {
            const data = data_read.last_data();
            console.log(data);
            if (data) {
                logfile.write(JSON.stringify(data) + "\n");
                res.write(`data: ${JSON.stringify(data)}\n\n`);
            } else {
                res.write("data: {}\n\n");
            }
        } catch (err) {
            console.log("Error in stream:", err);
            clearInterval(interval);
        }
    }, 500); 
    
    req.on("close", () => {
        clearInterval(interval);
        logfile.end();
    });
});

// ---------------------------------------------------------------------
// ROUTES
// ---------------------------------------------------------------------

// Render HTML
app.get("/", (req, res) => {
    res.sendFile(path.join(__dirname, "templates/page1.html"));
});

// ---------------------- POST /foo ------------------------------
app.post("/foo", (req, res) => {
    const data = req.body;

    gcp = []; 

    fs.writeFileSync("../data/data_log.txt", 
                     data.map(x => JSON.stringify(x)).join("\n"));

	const lastRow = data[data.length - 1];
	const len = lastRow.length;
	
	gcp.push([
	    [ lastRow[len - 1].lat, lastRow[len - 1].lng ],
	    [ lastRow[0].lat,       lastRow[0].lng ]
	]);

	for (let n = 1; n < len; n++) {
	    const segment = [
		[ lastRow[n - 1].lat, lastRow[n - 1].lng ],
		[ lastRow[n].lat,     lastRow[n].lng ]
	    ];
	    gcp.push(segment);
	}




    res.json(data);
});
const { spawn } = require("child_process");

// ---------------------- GET /path ------------------------------
app.get("/path", (req, res) => {
    const py = spawn("python3", ["src/main.py"]);

    py.stdin.write(JSON.stringify({ gcp }));
    py.stdin.end();

    let output = "";

    py.stdout.on("data", (data) => {
        const text = data.toString();
        console.log("[PYTHON STDOUT]:", text);
        output += text;
    });

    py.stderr.on("data", (data) => {
        console.log("[PYTHON ERROR]:", data.toString());
    });

    py.on("close", () => {
        
        const lines = output.trim().split(/\r?\n/);
        const lastLine = lines[lines.length - 1];

        try {
            const out = JSON.parse(lastLine);
            res.json({
                track: out.track,
                headland: out.headland
            });
        } catch (e) {
            console.log("JSON PARSE FAILED:", lastLine);
            res.status(500).json({ error: "Invalid Python output" });
        }
    });
});

//------------------------------------------------------------------------------
/*



*/











app.get("/test", (req, res) => {

	const { execFile } = require('child_process');

	const executablePath = './ntrip'; 
	//const args = ['eklntrip.escortskubota.com', 'arg2', 'arg3'];

	execFile(executablePath, args, (error, stdout, stderr) => {
	  if (error) {
	    console.error(`execFile error: ${error}`);
	    return;
	  }
	  if (stderr) {
	    console.error(`stderr: ${stderr}`);
	  }
	  console.log(`stdout: ${stdout}`);
	});

  
  
});


// ---------------------- GET /stop ------------------------------
app.get("/stop", (req, res) => {
    const response = proc.stopobject();
    res.json({ response });
});

// ---------------------- GET /simplify --------------------------
app.get("/simplify", (req, res) => {
    res.send("success");
});

// ---------------------------------------------------------------------

app.listen(3000, "0.0.0.0", () => {
    console.log("Server running on 0.0.0.0:3000");
});

