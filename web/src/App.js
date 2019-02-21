import React, {Component} from 'react';
import './App.css';
import LoginForm from "./LoginForm";
import ClubSelector from "./ClubSelector";
import RegisterFlow from "./RegisterFlow";
import Navbar from "./Components/Navbar";
import config from "./config";
import {handleFetchErrors} from "./utils";


class App extends Component {

    state = {
        authorization: undefined,
        register_to: undefined,
        message: {
            text: null,
            type: undefined
        },
        message_timeout: undefined,
        clubs: [],
        isLoadingClubs: false
    };

    componentDidMount() {
        let auth = localStorage.getItem("auth");
        let club = localStorage.getItem("club");
        let timeout = undefined;

        if (auth !== null) {
            let expiry = new Date(localStorage.getItem("auth_expiry"));
            timeout = setTimeout(this.resetAuthorization, expiry.getTime() - (new Date()).getTime());
        }

        this.setState({
            authorization: auth || undefined,
            register_to: club || undefined,
            auth_timeout: timeout
        });
    }

    deauthorize = () => {
        this.resetAuthorization("Your credentials were rejected by the server, please log back in and try again.")
    };


    render() {
        const isAuthorized = this.state.authorization !== undefined;
        const isClubSelected = this.state.register_to !== undefined && isAuthorized;
        return (
            <div>
                <Navbar
                    message={this.state.message}
                    isAuthorized={isAuthorized}
                    club={this.state.register_to}
                    onLogOff={this.resetAuthorization}
                    onChangeClub={this.updateClub}
                    onHideMessage={this.resetNotify}
                />
                {
                    !isAuthorized && <LoginForm
                        callback={this.setAuthorization}
                        notify={this.notify}
                    />
                }
                {
                    !isClubSelected && isAuthorized && <ClubSelector
                        callback={this.setRegisterTo}
                        clubs={this.state.clubs}
                        isLoadingClubs={this.state.isLoadingClubs}
                        triggerLoad={this.fetchClubList}
                    />
                }
                {
                    isClubSelected && isAuthorized &&
                    <RegisterFlow authorization={this.state.authorization}
                                  deauthorizationCallback={this.deauthorize}
                                  club={this.state.register_to}/>
                }
            </div>

        )
    }

    setAuthorization = (auth, remember, user) => {
        let expiry = new Date();
        user = user || "hope you have a great day!";
        if (remember) {
            expiry.setMonth(expiry.getMonth() + 1);
        } else {
            expiry.setHours(expiry.getHours() + 3);
        }
        console.log(expiry);
        let timeout = setTimeout(() => this.resetAuthorization("Your session has expired and you must log in again"), expiry.getTime() - (new Date()).getTime());
        this.setState({authorization: auth, auth_timeout: timeout});

        localStorage.setItem("auth", auth);
        localStorage.setItem("auth_expiry", expiry.toJSON());
        this.notify("Welcome, " + user, "success")
    };
    setRegisterTo = (club) => {
        this.setState({register_to: club});
        localStorage.setItem("club", club);
        this.notify(`You're registering new users into ${club}`, "success")

    };
    resetAuthorization = (message) => {
        if (!message) {
            message = "You've been logged out"
        }
        clearTimeout(this.state.auth_timeout);
        this.setState({
            authorization: undefined,
            auth_timeout: undefined,
            register_to: undefined
        });
        localStorage.removeItem("auth");
        localStorage.removeItem("auth_expiry");
        localStorage.removeItem("club");
        this.notify(message, "error")
    };

    updateClub = (club) => {
        if (!club) {
            localStorage.removeItem("club");
            club = undefined;
        } else {
            localStorage.setItem("club", club);
        }
        this.setState({
            register_to: club
        })
    };

    notify = (text, type) => {
        this.setState({
            message: {
                text: text,
                type: type,
                show: true,
            },
        })
    };

    resetNotify = () => {
        this.setState({
            message: {
                text: this.state.message.text,
                type: this.state.message.type,
                show: false
            }
        })
    };

    fetchClubList = () => {
        this.setState({
            isLoadingClubs: true
        });
        fetch(`${config.api}${config.endpoints.clubs}`, {
            headers: new Headers({
                Authorization: this.state.authorization
            })
        }).then(handleFetchErrors).then(data => {
            this.setState({
                clubs: data.data,
                isLoadingClubs: false
            })
        }).catch((err) => {
            console.log(err);
            if (err.message === "401") {
                console.log("Request DeAuth (401)");
                this.deauthorize();
            }
            this.setState({
                clubs: undefined,
                isLoadingClubs: false
            })
        })
    };

}

export default App;
