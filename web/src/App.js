import React, {Component} from 'react';
import './App.css';
import config from "./config"


class App extends Component {
    cleanStatus = {
        value: "Scan",
        extras: {},
        reset: {
            timeout: null,
            seconds: null,
        }
    };

    state = {
        club: "csit",
        status: this.cleanStatus

    };

    render() {
        let {club} = this.state;
        let status = this.state.status.value;

        const parent = {
            display: "flex",
            flexDirection: "column",
            width: "100%",
            height: "100%",
            position: "fixed"
        };

        const stream = {
            display: "flex",
            flexDirection: "column",
            height: "100%",
            width: "100%",
            backgroundColor: "black",
            position: 'relative'
        };

        const info = {
            display: "flex",
            flexDirection: "row",
            paddingBottom: "20px",
        };

        const infoCol1 = {
            display: "flex",
            flexDirection: "column",
            paddingLeft: 5,
            paddingRight: 5,
            marginRight: "auto",
        };

        const infoCol2 = {
            display: "flex",
            flexDirection: "column",
            paddingLeft: 5,
            paddingRight: 5,
            marginLeft: "auto",
            textAlign: "right",
            marginTop: "auto",
        };

        const colorMap = {
            "Found": "darkgreen",
            "Scanning": "darkblue",
            "Registering": "darkgreen",
            "RegistrationFailed": "darkred",
            "RegistrationSuccess": "darkgreen",
            "Errored": "darkred",
            "Blocked": "darkred",
        };

        const statusDescr = {
            Found: <i>Tap anywhere to register!</i>,
            Registering: <i>We are signing you up!</i>,
            Blocked: <b>Please allow access to the camera in order to sign up</b>,
            Errored: <b>This browser does not support camera access :(</b>,
            Scanning: <div>
                <i>Place your valid student ID in front of the camera.</i>
                <div><b>Make sure your name and student ID are clearly visible!</b></div>
            </div>,
            RegistrationFailed: <div>
                <i>We couldn't sign you up :(</i>
                <div><b>Reason: </b>?</div>
                <div>Tap to continue...</div>
            </div>,
            RegistrationSuccess: <div>
                <i>You've signed up to {club}</i>
                <div><b>Tap to dismiss...</b></div>
            </div>
        };

        let statusStyle = {
            color: colorMap[status],
        };

        let logo = {
            color: "#EE0026"
        };

        let isErr = ["Blocked", "Errored"].includes(status);

        return (
            <div style={parent}>
                <div id="stream-info" style={info}>
                    <div style={infoCol1}>
                        <div>
                            <h3>
                                <b style={logo}>SignMeUp</b> to rmit club "{club}"
                            </h3></div>
                        {
                            statusDescr[status]
                        }
                    </div>
                    <div style={infoCol2}>
                        <div style={statusStyle}>
                            <b style={{color: "white", backgroundColor: colorMap[status]}}>
                                {isErr ? "Offline" : "Online"}
                            </b> {colorMap.hasOwnProperty(status) && "-"} {status}</div>
                    </div>
                </div>

            </div>
        );
    }

    startCapture = (blob) => {
        let newStatus = {
            value: "Registering",
            extras: {},
            reset: {
                timeout: undefined,//setTimeout(this.resetState, 5000),
                seconds: Date.now() + 5000
            }
        };
        this.setState({
            status: newStatus
        });

        fetch(`${config.api}/register/${this.state.club}`, {
            method: "post",
            body: blob
        }).then((response) => {
            if (response.status !== 200) {
                throw Error("Bad status " + response.statusText)
            }
            return response.json()
        }).then((data) => {
            return {
                user: data.user,
                club: data.club,
                card: {
                    expiry: data.expiry
                }
            }
        }).then((extras) => {
            let newStatus = {
                value: "Registered",
                extras: extras,
                reset: {
                    timeout: setTimeout(() => this.setState({status: this.cleanStatus}), 5000),
                    seconds: Date.now() + 5000
                }
            };
            this.setState({
                status: newStatus
            })
        }).catch((error) => {
            console.log("Caught Error during capture process");
            console.log(error);
            newStatus = {
                value: "Error",
                extras: error,
                reset: {
                    timeout: setTimeout(() => this.setState({status: this.cleanStatus}), 5000),
                    seconds: Date.now() + 5000
                }
            }
        })

    };

}

export default App;
