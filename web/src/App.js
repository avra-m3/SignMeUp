import React, {Component} from 'react';
import './App.css';
import LoginForm from "./LoginForm";
import ClubSelector from "./ClubSelector";
import RegisterFlow from "./RegisterFlow";
import Navbar from "./Components/Navbar";


class App extends Component {

    state = {
        authorization: undefined,
        register_to: undefined,
        message: {
            text: null,
            type: undefined
        },
        message_timeout: undefined,
    };

    componentDidMount() {
        let auth = localStorage.getItem("auth");
        let club = localStorage.getItem("club");

        let expiry = new Date(localStorage.getItem("auth_expiry"));
        let timeout = setTimeout(this.resetAuthorization, expiry.getTime() - (new Date()).getTime());

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
                    onLogOff={this.resetAuthorization}
                    onHideMessage={this.resetNotify}
                    message={this.state.message}
                    isAuthorized={isAuthorized}
                    club={this.state.register_to}
                />
                {
                    !isAuthorized && <LoginForm
                        callback={this.setAuthorization}
                    />
                }
                {
                    !isClubSelected && isAuthorized && <ClubSelector
                        callback={this.setRegisterTo}
                        deauthorizationCallback={this.deauthorize}
                        authorization={this.state.authorization}
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
    }

}

export default App;
