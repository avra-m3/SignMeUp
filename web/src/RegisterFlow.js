import React, {Component} from 'react';
import * as PropTypes from "prop-types";
import {withStyles} from '@material-ui/core/styles';
import config from './config'
import CardCapture from "./Components/CardCapture";
import Loading from "./Components/Loading";
import Results from "./Components/Results";
import ErrorDisplay from "./Components/ErrorDisplay";
import {dataURItoBlob} from "./utils";


const styles = theme => ({
    root: {
        height: "100%",
    }

});


const modes = {
    // Show Camera
    capture: "capture",
    // Show loading
    retrieve: "retrieve",
    // Show data
    show: "show"
};


class RegisterFlow extends Component {
    /**
     * This Component handles everything to do with the registration flow, it is provided the club being registered
     * too as well as the authorization token to use in requests.
     * @type {{}}
     */

    state = {
        request: undefined
    };

    static propTypes = {
        deauthorizationCallback: PropTypes.func.isRequired,
        authorization: PropTypes.string.isRequired,
        club: PropTypes.string.isRequired

    };

    resetState = () => {
        this.setState({
            request: undefined
        })
    };

    render() {
        const {classes} = this.props;

        const isCapturing = this.state.request === undefined;
        const isRetrieving = !isCapturing && this.state.request.response === null;
        const isShowing = !isCapturing && !isRetrieving && !this.state.request.err;
        const isErred = !isCapturing && !isRetrieving && !isShowing;

        return (
            <div className={classes.root}>
                <CardCapture onCapture={this.onFakeCapture} show={isCapturing}/>
                {isRetrieving && <Loading/>}
                {isShowing && <Results
                    onContinue={this.resetState}
                    registration={this.state.request.response}
                    authorization={this.props.authorization}
                />}
                {isErred && <ErrorDisplay
                    onContinue={this.resetState}
                    onResend={() => this.onCapture(this.state.request.data)}
                    error={this.state.request.response}
                />}
            </div>
        )
    }

    onFakeCapture = (dataURI) => {
        this.setState({
            data: dataURI,
            err: null,
            response: null
        });

        fetch(`${config.api}/club/csit/register/3599575`, {
            headers: new Headers({
                "Authorization": this.props.authorization
            }),
        }).then((response) => {
            return response.json()
        }).then(data => {
            if (data.code === 200) {
                this.setState({
                    request: {
                        data: dataURI,
                        err: null,
                        response: data
                    }
                })
            } else {
                this.setState({
                    request: {
                        data: dataURI,
                        err: data.message,
                        response: data
                    }
                })
            }
        }).catch((error) => {
            this.setState({
                request: {
                    data: dataURI,
                    err: error.message,
                    response: {
                        code: undefined,
                        message: "An unexpected error occurred",
                        status: ""
                    }
                }
            })
        })
    };

    onCapture = (dataURI) => {
        let form = new FormData();
        let image = dataURItoBlob(dataURI);
        form.append("student_card", image, image.name);
        this.setState({
            request: {
                data: dataURI,
                err: null,
                response: null
            }
        });
        fetch(`${config.api}${config.endpoints.register.replace("{club_id}", this.props.club)}`, {
            method: "post",
            headers: new Headers({
                "Authorization": this.props.authorization
            }),
            body: form
        }).then((response) => {
            return response.json()
        }).then(data => {
            if (data.code === 200) {
                this.setState({
                    request: {
                        data: dataURI,
                        err: null,
                        response: data
                    }
                })
            } else {
                this.setState({
                    request: {
                        data: dataURI,
                        err: data.message,
                        response: data
                    }
                })
            }
        }).catch((error) => {
            this.setState({
                request: {
                    data: dataURI,
                    err: error.message,
                    response: {
                        code: undefined,
                        message: "An unexpected error occurred",
                        status: ""
                    }
                }
            })
        })
    };


}

export default withStyles(styles)(RegisterFlow);