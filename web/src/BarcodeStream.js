import React from 'react';
import Quagga from "quagga";
import PropTypes from "prop-types";
import ReactCountdownClock from "react-countdown-clock"


export default class BarcodeStream extends React.Component {

    static propTypes = {
        callback: PropTypes.func.isRequired,
        reset: PropTypes.func.isRequired,
        style: PropTypes.object,
        status: PropTypes.object,
        club: PropTypes.string
    };

    componentDidMount() {
        Quagga.init({
            inputStream: {
                name: "Live",
                type: "LiveStream",
                target: '#stream'
            },

            decoder: {
                readers: ["code_39_reader"],
            }
        }, function (err) {
            if (err) {
                console.log(err);
                return
            }

            Quagga.start();
        });


        Quagga.onDetected((data) => {
            if (data.codeResult.code.length === 14 && data.codeResult.code.startsWith("21259")) {
                // console.log(data);
                this.props.callback(data)
            }
        });
        Quagga.onProcessed(function (result) {
            let drawingCtx = Quagga.canvas.ctx.overlay,
                drawingCanvas = Quagga.canvas.dom.overlay;

            drawingCtx.clearRect(0, 0, parseInt(drawingCanvas.getAttribute("width")), parseInt(drawingCanvas.getAttribute("height")));
            if (result) {
                if (result.boxes) {
                    result.boxes.filter(function (box) {
                        return box !== result.box;
                    }).forEach(function (box) {
                        Quagga.ImageDebug.drawPath(box, {x: 0, y: 1}, drawingCtx, {color: "green", lineWidth: 2});
                    });
                }

                if (result.box) {
                    Quagga.ImageDebug.drawPath(result.box, {x: 0, y: 1}, drawingCtx, {color: "#00F", lineWidth: 2});
                }

                if (result.codeResult && result.codeResult.code) {
                    Quagga.ImageDebug.drawPath(result.line, {x: 'x', y: 'y'}, drawingCtx, {color: 'red', lineWidth: 3});
                }
            }
        });
    }

    render() {
        const overlay = {
            marginTop: "auto",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            top: 0,
            right: 0,
            bottom: 0,
            left: 0,
            height: "100%",
            position: "absolute"
        };


        let secondsToReset = (this.props.status.reset.seconds - Date.now()) / 1000;

        return <div id={"stream"} style={this.props.style}>
            <div style={overlay}>
                {this.props.status.reset.seconds !== null &&
                <div>
                    {this.props.status.value === "Found" && <b>Sign up {this.props.status.extras.user_id}?</b>}
                    <ReactCountdownClock seconds={secondsToReset}
                                         color="white"
                                         size={300}
                                         showMilliseconds={0}
                    />
                    <button onClick={this.props.reset}>Cancel</button>
                </div>
                }
            </div>
        </div>
    }
}
