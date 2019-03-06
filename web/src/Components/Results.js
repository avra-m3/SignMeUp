import React, {Component} from 'react';
import * as PropTypes from "prop-types";
import Paper from '@material-ui/core/Paper';
import {withStyles} from '@material-ui/core/styles';
import Typography from "@material-ui/core/Typography";
import InputLabel from "../../node_modules/@material-ui/core/InputLabel/InputLabel";
import Input from "../../node_modules/@material-ui/core/Input/Input";
import FormControl from "../../node_modules/@material-ui/core/FormControl/FormControl";
import Avatar from "../../node_modules/@material-ui/core/Avatar/Avatar";
import {AddCircle, Check, Close, Link} from '@material-ui/icons';
import CssBaseline from "../../node_modules/@material-ui/core/CssBaseline/CssBaseline";
import Button from "@material-ui/core/Button";
import config from "../config"
import Veil from "./Veil";
import CircularProgress from "../../node_modules/@material-ui/core/CircularProgress/CircularProgress";


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
        maxWidth: 400,
    },
    menu: {
        maxWidth: 400,
    },
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
    button: {
        margin: theme.spacing.unit,
    },
    rightIcon: {
        marginLeft: theme.spacing.unit,
    },
    progressRoot: {
        height: "100%",
        padding: 0,
        margin: 0,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
    },
    progress: {
        width: "auto"
    }
});


class Results extends Component {

    static propTypes = {
        onContinue: PropTypes.func.isRequired,
        registration: PropTypes.shape({
            id: PropTypes.number,
            expiry: PropTypes.string,
            club: PropTypes.shape({
                id: PropTypes.number,
                name: PropTypes.string,
                description: PropTypes.string
            }),
            user: PropTypes.shape({
                email: PropTypes.string,
                first_name: PropTypes.string,
                last_name: PropTypes.string,
                student_id: PropTypes.string
            })
        }).isRequired
    };

    state = {
        user_email: undefined,
        user_f_name: undefined,
        user_l_name: undefined,
        status: "edit"

    };

    handleChange = name => event => {
        this.setState({
            [name]: event.target.value,
        });
    };

    render() {
        const {classes, registration} = this.props;

        const {status} = this.state;

        const email = this.state.user_email === undefined ? registration.user.email : this.state.user_email;
        const first_name = this.state.user_f_name || registration.user.first_name;
        const last_name = this.state.user_l_name || registration.user.last_name;

        return (
            <main className={classes.main}>
                {status === "updating" && <Veil>
                    <div className={classes.progressRoot}>
                        <CircularProgress className={classes.progress}/>
                    </div>
                </Veil>}

                {status === ""}
                <CssBaseline/>
                <Paper className={classes.paper}>
                    <Avatar className={classes.avatar}>
                        <AddCircle/>
                    </Avatar>
                    <Typography component="h1" variant="h5">
                        New Registration
                    </Typography>
                    <Typography component="p">
                        Please confirm the users registration information below and update as required.
                    </Typography>


                    <form className={classes.form}
                          onSubmit={this.attemptLogin}
                    >
                        <FormControl margin="normal" fullWidth>
                            <InputLabel htmlFor="student_id">Student ID</InputLabel>
                            <Input id="student_id" name="student_id" value={registration.user.student_id}
                                   disabled/>
                        </FormControl>

                        <FormControl margin="normal" fullWidth>
                            <InputLabel htmlFor="first_name">First Name</InputLabel>
                            <Input id="first_name" name="first_name" value={first_name} autoFocus
                                   onChange={this.handleChange('user_f_name')}
                            />
                        </FormControl>

                        <FormControl margin="normal" fullWidth>
                            <InputLabel htmlFor="last_name">Last Name</InputLabel>
                            <Input id="last_name" name="last_name" value={last_name}
                                   onChange={this.handleChange('user_l_name')}
                            />
                        </FormControl>

                        <FormControl margin="normal" fullWidth>
                            <InputLabel htmlFor="email">Email Address</InputLabel>
                            <Input id="email" name="email" value={email}
                                   onChange={this.handleChange('user_email')}
                            />
                        </FormControl>
                    </form>

                    <Avatar className={classes.avatar}>
                        <Link/>
                    </Avatar>
                    <form className={classes.form}
                          onSubmit={this.attemptLogin}
                    >
                        <FormControl margin="normal" fullWidth>
                            <InputLabel htmlFor="club_name">Club Name</InputLabel>
                            <Input id="club_name" name="club_name" value={registration.club.name}
                                   disabled/>
                        </FormControl>
                        <FormControl margin="normal" fullWidth>
                            <InputLabel htmlFor="club_desc">Club Description</InputLabel>
                            <Input id="club_desc" name="club_desc" value={registration.club.description}
                                   disabled multiline/>
                        </FormControl>
                    </form>
                    <div>
                        <Button
                            variant="contained"
                            color="primary"
                            className={classes.button}
                            onClick={this.onUpdate}
                        >
                            Update <Check className={classes.rightIcon}/>
                        </Button>
                        <Button
                            variant="contained"
                            color="primary"
                            className={classes.button}
                            onClick={this.props.onContinue}
                        >
                            Continue <Close className={classes.rightIcon}/>
                        </Button>
                    </div>

                </Paper>
            </main>
        );
    }

    onUpdate = () => {
        const email = this.state.user_email === undefined ? this.props.registration.user.email : this.state.user_email;
        const first_name = this.state.user_f_name || this.props.registration.user.first_name;
        const last_name = this.state.user_l_name || this.props.registration.user.last_name;

        if (this.state.user_email === this.state.user_f_name === this.state.user_l_name === undefined) {
            this.setState({
                status: "updated"
            });
            setTimeout(this.props.onContinue(), 5000)
        }

        let data = {
            first_name: first_name,
            last_name: last_name,
            email: email,
        };


        this.setState({
            status: "updating"
        });


        fetch(`${config.api}${config.endpoints.user.replace("{user_id}", this.props.registration.user.student_id)}`, {
            method: "put",
            headers: new Headers({
                "Authorization": this.props.authorization,
                "Content-Type": "application/json",
            }),
            body: JSON.stringify(data)
        }).then((response) => {
            if (response.ok) {
                this.setState({
                    status: "updated"
                });
                setTimeout(this.props.onContinue(), 5000)
            } else {
                return response.json()
            }
        }).then((data) => {
            this.setState({
                status: "failed",
                reason: data.message
            });
            setTimeout(() => this.setState({status: "edit"}), 5000);
        }).catch(() => {
            this.setState({
                status: "failed",
            });
            setTimeout(() => this.setState({status: "edit"}), 5000);
        })
    }
}

export default withStyles(styles)(Results);