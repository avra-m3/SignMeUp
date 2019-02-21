import React, {Component} from 'react';
import * as PropTypes from "prop-types";
import Paper from '@material-ui/core/Paper';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';
import {withStyles} from '@material-ui/core/styles';
import config from './config'
import FormControlLabel from "../node_modules/@material-ui/core/FormControlLabel/FormControlLabel";
import FormControl from "../node_modules/@material-ui/core/FormControl/FormControl";
import InputLabel from "../node_modules/@material-ui/core/InputLabel/InputLabel";
import Input from "../node_modules/@material-ui/core/Input/Input";
import Avatar from "../node_modules/@material-ui/core/Avatar/Avatar";
import CssBaseline from "../node_modules/@material-ui/core/CssBaseline/CssBaseline";
import LockOutlinedIcon from '@material-ui/icons/LockOutlined';
import Checkbox from '@material-ui/core/Checkbox'


const styles = theme => ({
    main: {
        width: 'auto',
        display: 'block', // Fix IE 11 issue.
        marginLeft: theme.spacing.unit * 3,
        marginRight: theme.spacing.unit * 3,
        [theme.breakpoints.up(400 + theme.spacing.unit * 3 * 2)]: {
            width: 400,
            marginLeft: 'auto',
            marginRight: 'auto',
        },
    },
    paper: {
        marginTop: theme.spacing.unit * 8,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        padding: `${theme.spacing.unit * 2}px ${theme.spacing.unit * 3}px ${theme.spacing.unit * 3}px`,
    },
    avatar: {
        margin: theme.spacing.unit,
        backgroundColor: theme.palette.secondary.main,
    },
    form: {
        width: '100%', // Fix IE 11 issue.
        marginTop: theme.spacing.unit,
    },
    submit: {
        marginTop: theme.spacing.unit * 3,
    },
});


class LoginForm extends Component {

    state = {
        username: "",
        password: "",
        remember: false
    };

    static propTypes = {
        callback: PropTypes.func.isRequired,
        notify: PropTypes.func.isRequired
    };


    handleChange = name => event => {
        this.setState({
            [name]: event.target.value,
        });
    };

    handleCheckedChange = name => event => {
        this.setState({
            [name]: event.target.checked,
        });
    };

    render() {
        const {classes} = this.props;

        return (
            <main className={classes.main}>
                <CssBaseline/>
                <Paper className={classes.paper}>
                    <Avatar className={classes.avatar}>
                        <LockOutlinedIcon/>
                    </Avatar>
                    <Typography component="h1" variant="h5">
                        Sign in
                    </Typography>
                    <form className={classes.form}
                          onSubmit={this.attemptLogin}
                    >
                        <FormControl margin="normal" required fullWidth>
                            <InputLabel htmlFor="email">Email Address</InputLabel>
                            <Input id="email" name="email" autoComplete="email" autoFocus
                                   onChange={this.handleChange('username')}
                            />
                        </FormControl>
                        <FormControl margin="normal" required fullWidth>
                            <InputLabel htmlFor="password">Password</InputLabel>
                            <Input name="password" type="password" id="password" autoComplete="current-password"
                                   onChange={this.handleChange('password')}
                            />
                        </FormControl>
                        <FormControlLabel
                            control={
                                <Checkbox value="remember" color="primary"
                                          onChange={this.handleCheckedChange("remember")}
                                />}
                            label="Remember me"
                        />
                        <Button
                            type="submit"
                            fullWidth
                            variant="contained"
                            color="primary"
                            className={classes.submit}
                        >
                            Sign in
                        </Button>
                    </form>
                </Paper>
            </main>
        );
    }

    attemptLogin = (event) => {
        fetch(`${config.api}${config.endpoints.authorize}`, {
            headers: new Headers({
                'Authorization': 'Basic ' + btoa(`${this.state.username}:${this.state.password}`),
            })
        }).then((response) => {
            if (response.ok) {
                console.log("Running callback");
                return response.json()
            } else {
                this.props.notify(`We couldn't log you in with that (${response.status})`, "error");
                console.log(response)
            }
        }).then(data => {
            this.props.callback(`Bearer ${data.token}`, this.state.remember)
        }).catch(error => {
            console.log(error);
            this.props.notify("An error occurred while attempting to validate those credentials", "error")
        });
        event.preventDefault()
    }
}

export default withStyles(styles)(LoginForm);