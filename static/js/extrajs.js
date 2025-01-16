function cargarOpcionesYSeleccionar(paisId, selectorPais, selectorProvincia) {
            cargarPaises(selectorPais).then(function () {
                $(selectorPais).val(paisId).trigger('change.select2');
                return cargarProvincias(paisId, selectorProvincia);
            });
        }
        function cargarPaises(selectorPais) {
            return new Promise(function (resolve, reject) {
                $.ajax({
                    url: `/pais/list`,
                    type: 'GET',
                    dataType: 'json',
                    success: function (data) {
                        let options = data.paises.map(function (item) {
                            return `<option value="${item.key}">${item.value}</option>`;
                        });
                        $(selectorPais).html('<option value="">Seleccione</option>' + options.join(''));
                        resolve();
                    },
                    error: function (error) {
                        console.log('Error al cargar los países:', error);
                        reject(error);
                    }
                });
            });
        }
        function cargarProvincias(paisId, selectorProvincia) {
            return new Promise(function (resolve, reject) {
                $.ajax({
                    url: `/pais/${paisId}/provincias`,
                    type: 'GET',
                    dataType: 'json',
                    success: function (data) {
                        let options = data.provincias.map(function (item) {
                            return `<option value="${item.key}">${item.value}</option>`;
                        });
                        $(selectorProvincia).html('<option value="">Seleccione</option>' + options.join(''));
                        resolve();
                    },
                    error: function (error) {
                        console.log('Error al cargar las provincias:', error);
                        reject(error);
                    }
                });
            });
        }
        function cargarMunicipios(provinciaId, selectorMunicipio) {
                return new Promise(function(resolve, reject) {
                    $.ajax({
                        url: `/provincia/${provinciaId}/municipios`,
                        type: 'GET',
                        dataType: 'json',
                        success: function(data) {
                            let options = data.municipios.map(function(item) {
                                return `<option value="${item.key}">${item.value}</option>`;
                            });
                            $(selectorMunicipio).html('<option value="">Seleccione</option>' + options.join(''));
                            resolve();
                        },
                        error: function(error) {
                            console.log('Error al cargar los municipios:', error);
                            reject(error);
                        }
                    });
                });
            }
        function cargarSelect2() {
            $('#id_pais_add_cliente').select2({
                dropdownParent: $('#crear_persona_cliente'),
                minimumResultsForSearch: 2,
                selectOnClose: true,
                placeholder: 'Cuba',
                language: 'es'
            }).val('1').trigger('change').prop('disabled', true);
            $('#id_pais_add_cliente_hidden').val('1')
            cargarOpcionesYSeleccionar(1, '#id_pais_add_cliente', '#id_provincia_add_cliente')

            $('#id_provincia_add_cliente').select2({
                dropdownParent: $('#crear_persona_cliente'),
                minimumResultsForSearch: 2,
                selectOnClose: true,
                placeholder: 'Seleccione',
                language: 'es'
            }).on('select2:select', function () {
                let provincia_id = $(this).val();
                $('#id_municipio_add_cliente').removeAttr('disabled').val(null).trigger('change.select2');
                $('#id_municipio_add_cliente').select2({
                    dropdownParent: $('#crear_persona_cliente'),
                    minimumResultsForSearch: 2,
                    selectOnClose: true,
                    placeholder: 'Seleccione',
                    language: 'es',
                    ajax: {
                        url: `/provincia/${provincia_id}/municipios`,
                        dataType: 'json',
                        delay: 250,
                        data: function (params) {
                            return {q: params.term};
                        },
                        processResults: function (data) {
                            return {
                                results: $.map(data.municipios, function (item) {
                                    return {id: item.key, text: item.value};
                                })
                            };
                        },
                        cache: true
                    }
                });
            });
            $('#id_municipio_add_cliente').select2({
                dropdownParent: $('#crear_persona_cliente'),
                minimumResultsForSearch: 2,
                selectOnClose: true,
                placeholder: 'Seleccione',
                language: 'es'
            });
            $('#id_pais_add_remitente').select2({
                dropdownParent: $('#crear_persona_remitente'),
                minimumResultsForSearch: 2,
                selectOnClose: true,
                placeholder: 'Estados Unidos',
                language: 'es'
            }).val('2').trigger('change').prop('disabled', true);
            cargarOpcionesYSeleccionar(2, '#id_pais_add_remitente', '#id_provincia_add_remitente')
            $('#id_pais_add_remitente_hidden').val('2')

            $('#id_provincia_add_remitente').select2({
                dropdownParent: $('#crear_persona_remitente'),
                minimumResultsForSearch: 2,
                selectOnClose: true,
                placeholder: 'Seleccione',
                language: 'es'
            }).on('select2:select', function () {
                let provincia_id = $(this).val();
                $('#id_municipio_add_remitente').removeAttr('disabled').val(null).trigger('change.select2');
                $('#id_municipio_add_remitente').select2({
                    dropdownParent: $('#crear_persona_remitente'),
                    minimumResultsForSearch: 2,
                    selectOnClose: true,
                    placeholder: 'Seleccione',
                    language: 'es',
                    ajax: {
                        url: `/provincia/${provincia_id}/municipios`,
                        dataType: 'json',
                        delay: 250,
                        data: function (params) {
                            return {q: params.term};
                        },
                        processResults: function (data) {
                            return {
                                results: $.map(data.municipios, function (item) {
                                    return {id: item.key, text: item.value};
                                })
                            };
                        },
                        cache: true
                    }
                });
            });
            $('#id_municipio_add_remitente').select2({
                dropdownParent: $('#crear_persona_remitente'),
                minimumResultsForSearch: 2,
                selectOnClose: true,
                placeholder: 'Seleccione',
                language: 'es'
            });
            $('#id_pais_add_destinatario').select2({
                dropdownParent: $('#crear_persona_destinatario'),
                minimumResultsForSearch: 2,
                selectOnClose: true,
                placeholder: 'Cuba',
                language: 'es'
            }).val('1').trigger('change').prop('disabled', true);
            cargarOpcionesYSeleccionar(1, '#id_pais_add_destinatario', '#id_provincia_add_destinatario')
            $('#id_pais_add_destinatario_hidden').val('1')

            $('#id_provincia_add_destinatario').select2({
                dropdownParent: $('#crear_persona_destinatario'),
                minimumResultsForSearch: 2,
                selectOnClose: true,
                placeholder: 'Seleccione',
                language: 'es'
            }).on('select2:select', function () {
                let provincia_id = $(this).val();
                $('#id_municipio_add_destinatario').removeAttr('disabled').val(null).trigger('change.select2');
                $('#id_municipio_add_destinatario').select2({
                    dropdownParent: $('#crear_persona_destinatario'),
                    minimumResultsForSearch: 2,
                    selectOnClose: true,
                    placeholder: 'Seleccione',
                    language: 'es',
                    ajax: {
                        url: `/provincia/${provincia_id}/municipios`,
                        dataType: 'json',
                        delay: 250,
                        data: function (params) {
                            return {q: params.term};
                        },
                        processResults: function (data) {
                            return {
                                results: $.map(data.municipios, function (item) {
                                    return {id: item.key, text: item.value};
                                })
                            };
                        },
                        cache: true
                    }
                });
            });
            $('#id_municipio_add_destinatario').select2({
                dropdownParent: $('#crear_persona_destinatario'),
                minimumResultsForSearch: 2,
                selectOnClose: true,
                placeholder: 'Seleccione',
                language: 'es'
            });
        }
        $(document).ready(function () {
            cargarSelect2();
        });