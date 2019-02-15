import React, {Component} from 'react';
import './App.css';
import LoginForm from "./LoginForm";
import ClubSelector from "./ClubSelector";
import RegisterFlow from "./RegisterFlow";


class App extends Component {

    state = {
        authorization: undefined,
        register_to: undefined,
    };

    componentDidMount() {
        let auth = localStorage.getItem("auth");
        let club = localStorage.getItem("club");

        let expiry = new Date(localStorage.getItem("auth_expiry"));
        let timeout = setTimeout(this.resetAuthorization, expiry);

        this.setState({
            authorization: auth || undefined,
            register_to: club || undefined,
            auth_timeout: timeout
        })
    }


    render() {
        const isAuthorized = this.state.authorization !== undefined;
        const isClubSelected = this.state.register_to !== undefined && isAuthorized;
        return (
            <div>
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

    setAuthorization = auth => remember => {
        let expiry = new Date();

        if (remember) {
            expiry.setMonth(expiry.getMonth() + 1);
        } else {
            expiry.setHours(expiry.getHours() + 3);
        }

        let timeout = setTimeout(this.resetAuthorization, expiry);
        this.setState({authorization: auth, auth_timeout: timeout});

        localStorage.setItem("auth", auth);
        localStorage.setItem("auth_expiry", expiry.toJSON());


    };
    setRegisterTo = (club) => {
        this.setState({register_to: club});
        localStorage.setItem("club", club)
    };
    resetAuthorization = () => {
        clearTimeout(this.state.auth_timeout);
        this.setState({
            authorization: undefined,
            auth_timeout: undefined,
        });
        localStorage.removeItem("auth");
        localStorage.removeItem("auth_expiry");
    }


}

export default App;
