package org.cowco.cerberus.entities.responses;

public class LoginResponse {
    private final String jwt;

    public LoginResponse(String jwt) {
        this.jwt = jwt;
    }

    public String getJWT() {
        return jwt;
    }
}
