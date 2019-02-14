import React, {Component} from 'react';
import './App.css';
import LoginForm from "./LoginForm";
import ClubSelector from "./ClubSelector";

const modes = {
    capture: "capture",
    retrieve: "retrieve"
};

class App extends Component {

    state = {
        mode: modes.capture,
        authorization: undefined,
        register_to: undefined,
    };

    componentDidMount(){
        let auth = localStorage.getItem("auth");
        let club = localStorage.getItem("club");
        this.setState({
            authorization: auth || undefined,
            register_to: club || undefined
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
            </div>

        )
    }

    setAuthorization = (auth) => {
        this.setState({authorization: auth});
        localStorage.setItem("auth", auth)
    };
    setRegisterTo = (club) => {
        this.setState({register_to: club});
        localStorage.setItem("club", club)
    };
    setRegistration = (club) => this.setState({register_to: club});
    resetAuthorization = () => this.setState({authorization: undefined})


}

export default App;
