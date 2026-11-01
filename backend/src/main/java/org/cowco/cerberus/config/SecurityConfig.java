package org.cowco.cerberus.config;

import org.cowco.cerberus.middleware.AuthEntrypoint;
import org.cowco.cerberus.middleware.JwtAuthenticationFilter;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.annotation.web.configurers.AbstractHttpConfigurer;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;

@Configuration 
@EnableWebSecurity
public class SecurityConfig {
    @Autowired 
    private JwtAuthenticationFilter jwtFilter;
    @Autowired 
    private AuthEntrypoint authEntrypoint;

    /**
     * Beacon endpoint specifically allows any connections since the implants should not need to authenticate
     * (at least...for now)
     */
    @Bean 
    public SecurityFilterChain beaconSec(HttpSecurity http) throws Exception {
        http.securityMatcher("/beacon")
            .authorizeHttpRequests((auth) -> auth.anyRequest().permitAll()).csrf(AbstractHttpConfigurer::disable);
        return http.build();
    }

    @Bean 
    public SecurityFilterChain csrfSec(HttpSecurity http) throws Exception {
        http.securityMatcher("/csrf")
            .authorizeHttpRequests((auth) -> auth.anyRequest().permitAll()).csrf(AbstractHttpConfigurer::disable);
        return http.build();
    }

    @Bean 
    public SecurityFilterChain defaultSec(HttpSecurity http) throws Exception {
        // TODO Require admin permissions for create/delete/modify user
        http
            .securityMatcher(
                "/implants", 
                "/implants/**",
                "/task-types",
                "/task-types/**",
                "/tasks",
                "/tasks/**",
                "/users",
                "/users/**"
            )
            .authorizeHttpRequests((auth) -> auth
                .anyRequest()
                .authenticated()
            )
            .exceptionHandling(exception -> exception.authenticationEntryPoint(authEntrypoint))
            .sessionManagement(session -> session.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
            .addFilterBefore(jwtFilter, UsernamePasswordAuthenticationFilter.class);
        return http.build();
    }

    @Bean 
    protected PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }
}
