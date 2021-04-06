begin tran


DELETE FROM dbo.d_direcciones
    WHERE CodDir in ( 
				select CodDir from (
					select  *
					,ROW_NUMBER() OVER(PARTITION BY CodDir,CodDireccion	,CodPais	,CodProvincia,CodigoPostal	,CodLocalidad	,Localidad	,CodTipoDomicilio	,CalleNombre	,CalleNro	,Piso	,Departamento	,Manzana	,Origen	,AddressBookUID	,CodDireccionSocioPC ,FechaActualizacion 
					ORDER BY CodDireccion ASC) as  Position
					from d_direcciones 
				)b
				where Position>1				
				);

	select count(*) from d_direcciones
	select count(*) from (select distinct * from d_direcciones) b

	commit;

	rollback;