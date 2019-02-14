import React, {Component} from 'react';
import * as PropTypes from "prop-types";
import Paper from '@material-ui/core/Paper';
import Typography from '@material-ui/core/Typography';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import Icon from '@material-ui/core/Icon';
import {withStyles} from '@material-ui/core/styles';
import Camera from 'react-html5-camera-photo';
import config from './config'
import CardCapture from "./Components/CardCapture";
import {handleFetchErrors} from "./utils";
import Loading from "./Components/Loading";
import Results from "./Components/Results";
import ErrorDisplay from "./Components/ErrorDisplay";


const styles = theme => ({
    root:{
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

    render() {
        const {classes} = this.props;

        const isCapturing = this.state.request === undefined;
        const isRetrieving = !isCapturing && this.state.request.response === null;
        const isShowing = !isCapturing && !isRetrieving && this.state.request.err === null;
        const isErred = !isCapturing && !isRetrieving && !isCapturing;

        return (
            <div className={classes.root}>
                <Paper>
                    {isCapturing && <CardCapture onCapture={this.onCapture}/>}
                    {isRetrieving && <Loading/>}
                    {isShowing && <Results onContinue={this.resetState} registration={this.state.request.response}/>}
                    {isErred && <ErrorDisplay onContinue={this.resetState} error={this.state.request.response}/>}
                </Paper>
            </div>
        )
    }

    resetState = () => {
        this.setState({
            request: undefined
        })
    };

    onCapture = (image) => {
        let form = new FormData();
        form.append("student_card", image);
        this.setState({
            request: {
                data: form,
                err: null,
                response: null
            }
        });
        fetch(`${config.api}${config.endpoints.register.format(this.props.club)}`, {
            method: "post",
            headers: new Headers({
                "Authorization": this.props.authorization
            }),
            body: form
        }).then((response) => {
            if(response.ok){
                this.setState({
                    request: {
                        data: form,
                        err: null,
                        response: response.json()
                    }
                })
            }else{
                this.setState({
                    request: {
                        data: form,
                        err: response.statusText,
                        response: response.json()
                    }
                })
            }
        })
    }


}

export default withStyles(styles)(RegisterFlow);