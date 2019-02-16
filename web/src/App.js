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

                />
                {
                    !isAuthorized && <LoginForm
                        callback={this.setAuthorization}
                    />
                }
                {
                    !isClubSelected && isAuthorized && <ClubSelector
                        callback={this.setRegisterTo}
                        deauthorizationCallback={this.resetAuthorization}
                        authorization={this.state.authorization}
                    />
                }
                {
                    isClubSelected && isAuthorized &&
                    <RegisterFlow authorization={this.state.authorization}
                                  deauthorizationCallback={this.resetAuthorization}
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

        let timeout = setTimeout(this.resetAuthorization, expiry.getTime() - (new Date()).getTime());
        this.setState({authorization: auth, auth_timeout: timeout});

        localStorage.setItem("auth", auth);
        localStorage.setItem("auth_expiry", expiry.toJSON());
        this.notify("Welcome, " + user, "success")
    };
    setRegisterTo = (club) => {
        this.setState({register_to: club});
        localStorage.setItem("club", club);
        this.notify(`You're registering new users into ${club}`, "error")

    };
    resetAuthorization = () => {
        console.log("Expiring credentials");
        clearTimeout(this.state.auth_timeout);
        this.setState({
            authorization: undefined,
            auth_timeout: undefined,
        });
        localStorage.removeItem("auth");
        localStorage.removeItem("auth_expiry");
        localStorage.removeItem("club");
        this.notify("You've been logged out", "error")
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
