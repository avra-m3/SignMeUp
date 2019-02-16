import React, {Component} from 'react';
import * as PropTypes from "prop-types";
import Paper from '@material-ui/core/Paper';
import {withStyles} from '@material-ui/core/styles';
import config from './config'
import CardCapture from "./Components/CardCapture";
import Loading from "./Components/Loading";
import Results from "./Components/Results";
import ErrorDisplay from "./Components/ErrorDisplay";
import {dataURItoBlob} from "./utils";


const styles = theme => ({
    root: {}

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

    onCapture = (dataURI) => {
        let form = new FormData();
        let image = dataURItoBlob(dataURI);
        form.append("student_card", image, image.name);
        this.setState({
            request: {
                data: form,
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
                        data: form,
                        err: null,
                        response: data
                    }
                })
            } else {
                this.setState({
                    request: {
                        data: form,
                        err: data.message,
                        response: data
                    }
                })
            }
        }).catch((error) => {
            this.setState({
                request: {
                    data: form,
                    err: error.message,
                    response: {
                        code: -1,
                        message: "An unexpected error occurred",
                        status: ""
                    }
                }
            })
        })
    };

    render() {
        const {classes} = this.props;

        const isCapturing = this.state.request === undefined;
        const isRetrieving = !isCapturing && this.state.request.response === null;
        const isShowing = !isCapturing && !isRetrieving && !this.state.request.err;
        const isErred = !isCapturing && !isRetrieving && !isCapturing;

        return (
            <div className={classes.root}>
                <Paper>
                    <CardCapture onCapture={this.onCapture} show={isCapturing}/>
                    {isRetrieving && <Loading/>}
                    {isShowing && <Results onContinue={this.resetState} registration={this.state.request.response}/>}
                    {isErred && <ErrorDisplay onContinue={this.resetState} error={this.state.request.response}/>}
                </Paper>
            </div>
        )
    }


}

export default withStyles(styles)(RegisterFlow);