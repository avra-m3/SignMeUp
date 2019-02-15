import React, {Component} from 'react';
import * as PropTypes from "prop-types";
import Paper from '@material-ui/core/Paper';
import Typography from '@material-ui/core/Typography';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import Icon from '@material-ui/core/Icon';
import {withStyles} from '@material-ui/core/styles';
import config from './config'


const styles = theme => ({
    root: theme.mixins.gutters({
        paddingTop: 16,
        paddingBottom: 16,
        marginTop: theme.spacing.unit * 3,
    }),
    container: {
        display: 'flex',
        flexWrap: 'wrap',
        flexDirection: "column",
        margin: "auto",
        maxWidth: "200px"
    },
    textField: {
        marginLeft: theme.spacing.unit,
        marginRight: theme.spacing.unit,
        width: 200,
    },
    menu: {
        width: 200,
    },
});


class LoginForm extends Component {

    state = {
        username: "",
        password: ""
    };

    static propTypes = {
        callback: PropTypes.func.isRequired
    };


    handleChange = name => event => {
        this.setState({
            [name]: event.target.value,
        });
    };

    render() {
        const {classes} = this.props;

        return (
            <Paper className={classes.root}>
                <Typography variant="headline" elevation={4}>Login to continue</Typography>
                <form className={classes.container}>
                    <TextField
                        id="username-input"
                        label="Username"
                        type="username"
                        autoComplete="username"
                        margin="normal"
                        onChange={this.handleChange('username')}
                        className={classes.textField}
                    />
                    <TextField
                        id="password-input"
                        label="Password"
                        type="password"
                        autoComplete="current-password"
                        margin="normal"
                        onChange={this.handleChange('password')}
                        className={classes.textField}
                    />
                    <Button variant="contained" color="primary" onClick={this.attemptLogin}>
                        Login
                        <Icon>send</Icon>
                    </Button>
                </form>
            </Paper>
        )
    }

    attemptLogin = () => {
        fetch(`${config.api}${config.endpoints.authorize}`, {
            headers: new Headers({
                'Authorization': 'Basic ' + btoa(`${this.state.username}:${this.state.password}`),
            })
        }).then((response) => {
            if (response.status === 200) {
                this.props.callback('Basic ' + btoa(`${this.state.username}:${this.state.password}`))
            } else {
                this.setState({
                    result: response.status
                });
                console.log(response)
            }
        }).catch(error => {
            this.setState({
                result: error.valueOf()
            });
            console.log(error)
        })
    }
}

export default withStyles(styles)(LoginForm);