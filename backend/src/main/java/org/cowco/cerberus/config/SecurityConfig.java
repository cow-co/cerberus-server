package org.cowco.cerberus.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.core.annotation.Order;
import org.springframework.security.config.Customizer;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.annotation.web.configurers.AbstractHttpConfigurer;
import org.springframework.security.web.SecurityFilterChain;

@Configuration 
@EnableWebSecurity
public class SecurityConfig {
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
    public SecurityFilterChain implantSec(HttpSecurity http) throws Exception {
        http.securityMatcher("/implants", "/implants/**")
            .authorizeHttpRequests((auth) -> auth
                .anyRequest()
                .authenticated()
            ).httpBasic(Customizer.withDefaults());
        return http.build();
    }
}
