import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from models.producto import Producto
from models.movimiento import Movimiento

class LoginWindow:
    def __init__(self, db):
        self.db = db
        self.root = tk.Tk()
        self.root.title("Login - Sistema de Inventario Dental")
        self.root.geometry("300x200")
        self.root.resizable(False, False)
        self.crear_widgets()
    
    def crear_widgets(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="Sistema de Inventario Dental", font=('Arial', 12, 'bold')).pack(pady=10)
        
        ttk.Label(main_frame, text="Usuario:").pack(pady=5)
        self.entry_usuario = ttk.Entry(main_frame, width=20)
        self.entry_usuario.pack(pady=5)
        self.entry_usuario.focus()
        
        ttk.Label(main_frame, text="Contraseña:").pack(pady=5)
        self.entry_password = ttk.Entry(main_frame, width=20, show="*")
        self.entry_password.pack(pady=5)
        
        ttk.Button(main_frame, text="Ingresar", command=self.validar_login).pack(pady=10)
        
        self.root.bind('<Return>', lambda event: self.validar_login())
    
    def validar_login(self):
        usuario = self.entry_usuario.get()
        password = self.entry_password.get()
        
        if not usuario or not password:
            messagebox.showerror("Error", "Complete todos los campos")
            return
        
        from models.usuario import Usuario
        usuario_obj = Usuario.validar_login(self.db, usuario, password)
        
        if usuario_obj:
            self.root.destroy()
            MainWindow(self.db, usuario)
        else:
            messagebox.showerror("Error", "Credenciales incorrectas")
    
    def run(self):
        self.root.mainloop()

class MainWindow:
    def __init__(self, db, usuario):
        self.db = db
        self.usuario = usuario
        self.root = tk.Tk()
        self.root.title(f"Sistema de Inventario Dental - Usuario: {usuario}")
        self.root.geometry("1000x600")
        self.crear_menu()
        self.crear_widgets()
        self.actualizar_lista_productos()
        self.verificar_alertas()
    
    def crear_menu(self):
        menubar = tk.Menu(self.root)
        
        menu_archivo = tk.Menu(menubar, tearoff=0)
        menu_archivo.add_command(label="Salir", command=self.root.quit)
        
        menu_inventario = tk.Menu(menubar, tearoff=0)
        menu_inventario.add_command(label="Agregar Producto", command=self.agregar_producto)
        menu_inventario.add_command(label="Editar Producto", command=self.editar_producto)
        menu_inventario.add_command(label="Reponer Stock", command=self.reponer_stock)
        menu_inventario.add_command(label="Retirar Producto", command=self.retirar_producto)
        menu_inventario.add_separator()
        menu_inventario.add_command(label="Eliminar Producto", command=self.eliminar_producto)
        menu_inventario.add_separator()
        menu_inventario.add_command(label="Actualizar Lista", command=self.actualizar_lista_productos)
        
        menubar.add_cascade(label="Archivo", menu=menu_archivo)
        menubar.add_cascade(label="Inventario", menu=menu_inventario)
        
        self.root.config(menu=menubar)
    
    def crear_widgets(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        title_label = ttk.Label(main_frame, text="INVENTARIO ACTUAL - CLINICA DENTAL", 
                               font=('Arial', 14, 'bold'))
        title_label.pack(pady=(0, 10))
        
        table_frame = ttk.Frame(main_frame)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ('ID', 'Nombre', 'Categoria', 'Stock', 'Minimo', 'Precio', 'Estado')
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=20)
        
        column_widths = {
            'ID': 50, 'Nombre': 250, 'Categoria': 150, 
            'Stock': 80, 'Minimo': 80, 'Precio': 100, 'Estado': 120
        }
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=column_widths.get(col, 100))
        
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(button_frame, text="Agregar Producto", command=self.agregar_producto).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Editar Producto", command=self.editar_producto).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Reponer Stock", command=self.reponer_stock).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Retirar Producto", command=self.retirar_producto).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Eliminar Producto", command=self.eliminar_producto).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Actualizar", command=self.actualizar_lista_productos).pack(side=tk.LEFT, padx=5)
    
    def actualizar_lista_productos(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        productos = Producto.obtener_todos(self.db)
        
        for producto in productos:
            estado = "NORMAL"
            if producto.stock_actual == 0:
                estado = "AGOTADO"
            elif producto.necesita_reabastecimiento():
                estado = "BAJO STOCK"
            
            self.tree.insert('', 'end', values=(
                producto.id_producto,
                producto.nombre,
                producto.categoria,
                producto.stock_actual,
                producto.stock_minimo,
                f"${producto.precio_unitario:.2f}",
                estado
            ))
    
    def editar_producto(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Seleccione un producto para editar")
            return
        
        item_data = self.tree.item(selected_item[0])['values']
        producto_id = item_data[0]
        
        producto = Producto.buscar_por_id(self.db, producto_id)
        if not producto:
            messagebox.showerror("Error", "Producto no encontrado")
            return
        
        edit_window = tk.Toplevel(self.root)
        edit_window.title(f"Editar Producto - {producto.nombre}")
        edit_window.geometry("450x500")
        edit_window.resizable(False, False)
        edit_window.transient(self.root)
        edit_window.grab_set()
        
        main_frame = ttk.Frame(edit_window, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="EDITAR PRODUCTO", font=('Arial', 12, 'bold')).pack(pady=10)
        
        campos = [
            ("Nombre del Producto:", "entry_nombre", producto.nombre),
            ("Descripcion:", "entry_descripcion", producto.descripcion or ""),
            ("Categoria:", "entry_categoria", producto.categoria or ""),
            ("Stock Actual:", "entry_stock", str(producto.stock_actual)),
            ("Stock Minimo (alerta):", "entry_stock_min", str(producto.stock_minimo)),
            ("Precio Unitario ($):", "entry_precio", f"{producto.precio_unitario:.2f}")
        ]
        
        entries = {}
        
        for label, key, valor in campos:
            ttk.Label(main_frame, text=label).pack(pady=2)
            if "Descripcion" in label:
                entry = tk.Text(main_frame, width=40, height=3, font=('Arial', 9))
                entry.pack(pady=2)
                entry.insert("1.0", valor)
            else:
                entry = ttk.Entry(main_frame, width=30, font=('Arial', 10))
                entry.pack(pady=2)
                entry.insert(0, valor)
            entries[key] = entry
        
        def guardar_cambios():
            try:
                nombre_nuevo = entries['entry_nombre'].get().strip()
                descripcion = entries['entry_descripcion'].get("1.0", tk.END).strip() if hasattr(entries['entry_descripcion'], 'get') else entries['entry_descripcion'].get().strip()
                categoria = entries['entry_categoria'].get().strip()
                stock = int(entries['entry_stock'].get())
                stock_min = int(entries['entry_stock_min'].get())
                precio = float(entries['entry_precio'].get())
                
                if not nombre_nuevo:
                    messagebox.showerror("Error", "El nombre del producto es obligatorio")
                    return
                
                if stock < 0 or stock_min < 0:
                    messagebox.showerror("Error", "Los valores de stock no pueden ser negativos")
                    return
                
                if precio < 0:
                    messagebox.showerror("Error", "El precio no puede ser negativo")
                    return
                
                if nombre_nuevo.lower() != producto.nombre.lower():
                    query_check = "SELECT COUNT(*) FROM productos WHERE UPPER(nombre) = UPPER(:1) AND id_producto != :2"
                    cursor = self.db.execute_query(query_check, (nombre_nuevo, producto_id))
                    if cursor:
                        count = cursor.fetchone()[0]
                        if count > 0:
                            messagebox.showerror("Error", f"Ya existe otro producto con el nombre: {nombre_nuevo}")
                            return
                
                query = """
                UPDATE productos SET 
                    nombre = :1, 
                    descripcion = :2, 
                    categoria = :3, 
                    stock_actual = :4, 
                    stock_minimo = :5, 
                    precio_unitario = :6
                WHERE id_producto = :7
                """
                self.db.execute_query(query, (nombre_nuevo, descripcion, categoria, stock, stock_min, precio, producto_id))
                
                messagebox.showinfo("Exito", "Producto actualizado correctamente")
                edit_window.destroy()
                self.actualizar_lista_productos()
                
            except ValueError:
                messagebox.showerror("Error", "Verifique que los valores numericos sean correctos")
            except Exception as e:
                messagebox.showerror("Error", f"Error al guardar: {str(e)}")
        
        ttk.Button(main_frame, text="Guardar Cambios", command=guardar_cambios).pack(pady=15)
        ttk.Button(main_frame, text="Cancelar", command=edit_window.destroy).pack(pady=5)
    
    def eliminar_producto(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Seleccione un producto para eliminar")
            return
        
        item_data = self.tree.item(selected_item[0])['values']
        producto_id = item_data[0]
        producto_nombre = item_data[1]
        
        respuesta = messagebox.askyesno("Confirmar Eliminacion", 
                                       f"¿Está seguro de eliminar el producto:\n{producto_nombre}?\n\nEsta accion no se puede deshacer.")
        
        if respuesta:
            try:
                query_movimientos = "DELETE FROM movimientos WHERE id_producto = :1"
                self.db.execute_query(query_movimientos, (producto_id,))
                
                query_producto = "DELETE FROM productos WHERE id_producto = :1"
                self.db.execute_query(query_producto, (producto_id,))
                
                messagebox.showinfo("Exito", "Producto eliminado correctamente")
                self.actualizar_lista_productos()
                
            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar: {str(e)}")
    
    def reponer_stock(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Seleccione un producto para reponer stock")
            return
        
        item_data = self.tree.item(selected_item[0])['values']
        producto_id = item_data[0]
        producto_nombre = item_data[1]
        stock_actual = item_data[3]
        
        producto = Producto.buscar_por_id(self.db, producto_id)
        if not producto:
            messagebox.showerror("Error", "Producto no encontrado")
            return
        
        reponer_window = tk.Toplevel(self.root)
        reponer_window.title(f"Reponer Stock - {producto_nombre}")
        reponer_window.geometry("400x250")
        reponer_window.resizable(False, False)
        reponer_window.transient(self.root)
        reponer_window.grab_set()
        
        main_frame = ttk.Frame(reponer_window, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text=f"Producto: {producto_nombre}", font=('Arial', 10, 'bold')).pack(pady=5)
        ttk.Label(main_frame, text=f"Stock actual: {stock_actual}", font=('Arial', 9)).pack(pady=2)
        
        ttk.Separator(main_frame, orient='horizontal').pack(fill=tk.X, pady=10)
        
        ttk.Label(main_frame, text="Cantidad a agregar:").pack(pady=5)
        entry_cantidad = ttk.Entry(main_frame, width=10, font=('Arial', 10))
        entry_cantidad.pack(pady=5)
        entry_cantidad.focus()
        
        ttk.Label(main_frame, text="Proveedor:").pack(pady=5)
        entry_proveedor = ttk.Entry(main_frame, width=30, font=('Arial', 10))
        entry_proveedor.pack(pady=5)
        
        def confirmar_reposicion():
            try:
                cantidad = int(entry_cantidad.get())
                proveedor = entry_proveedor.get().strip()
                
                if cantidad <= 0:
                    messagebox.showerror("Error", "La cantidad debe ser mayor a 0")
                    return
                
                if not proveedor:
                    messagebox.showerror("Error", "Debe especificar el proveedor")
                    return
                
                nuevo_stock = stock_actual + cantidad
                producto.actualizar_stock(self.db, nuevo_stock)
                
                Movimiento.registrar_movimiento(
                    self.db, producto_id, 'ENTRADA', cantidad, 
                    f"Reposicion por: {proveedor}", "Sistema", self.usuario
                )
                
                messagebox.showinfo("Exito", f"Se agregaron {cantidad} unidades a {producto_nombre}")
                reponer_window.destroy()
                self.actualizar_lista_productos()
                self.verificar_alertas()
                
            except ValueError:
                messagebox.showerror("Error", "La cantidad debe ser un numero valido")
        
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=15)
        
        ttk.Button(button_frame, text="Confirmar Reposicion", command=confirmar_reposicion).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancelar", command=reponer_window.destroy).pack(side=tk.RIGHT, padx=5)
        
        reponer_window.bind('<Return>', lambda event: confirmar_reposicion())
    
    def retirar_producto(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Seleccione un producto para retirar")
            return
        
        item_data = self.tree.item(selected_item[0])['values']
        producto_id = item_data[0]
        producto_nombre = item_data[1]
        stock_actual = item_data[3]
        
        producto = Producto.buscar_por_id(self.db, producto_id)
        if not producto:
            messagebox.showerror("Error", "Producto no encontrado")
            return
        
        retiro_window = tk.Toplevel(self.root)
        retiro_window.title(f"Retirar Producto - {producto_nombre}")
        retiro_window.geometry("400x350")
        retiro_window.resizable(False, False)
        retiro_window.transient(self.root)
        retiro_window.grab_set()
        
        main_frame = ttk.Frame(retiro_window, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text=f"Producto: {producto_nombre}", font=('Arial', 10, 'bold')).pack(pady=5)
        ttk.Label(main_frame, text=f"Stock disponible: {stock_actual}", font=('Arial', 9)).pack(pady=2)
        
        ttk.Separator(main_frame, orient='horizontal').pack(fill=tk.X, pady=10)
        
        ttk.Label(main_frame, text="Cantidad a retirar:").pack(pady=5)
        entry_cantidad = ttk.Entry(main_frame, width=10, font=('Arial', 10))
        entry_cantidad.pack(pady=5)
        entry_cantidad.focus()
        
        ttk.Label(main_frame, text="Motivo del retiro:").pack(pady=5)
        entry_motivo = ttk.Entry(main_frame, width=40, font=('Arial', 10))
        entry_motivo.pack(pady=5)
        
        ttk.Label(main_frame, text="Doctor responsable:").pack(pady=5)
        entry_doctor = ttk.Entry(main_frame, width=30, font=('Arial', 10))
        entry_doctor.pack(pady=5)
        
        def confirmar_retiro():
            try:
                cantidad = int(entry_cantidad.get())
                motivo = entry_motivo.get().strip()
                doctor = entry_doctor.get().strip()
                
                if cantidad <= 0:
                    messagebox.showerror("Error", "La cantidad debe ser mayor a 0")
                    return
                
                if cantidad > stock_actual:
                    messagebox.showerror("Error", "No hay suficiente stock disponible")
                    return
                
                if not motivo:
                    messagebox.showerror("Error", "Debe especificar el motivo del retiro")
                    return
                
                if not doctor:
                    messagebox.showerror("Error", "Debe especificar el doctor responsable")
                    return
                
                nuevo_stock = stock_actual - cantidad
                producto.actualizar_stock(self.db, nuevo_stock)
                
                Movimiento.registrar_movimiento(
                    self.db, producto_id, 'SALIDA', cantidad, 
                    motivo, doctor, self.usuario
                )
                
                messagebox.showinfo("Exito", f"Se retiraron {cantidad} unidades de {producto_nombre}")
                retiro_window.destroy()
                self.actualizar_lista_productos()
                self.verificar_alertas()
                
            except ValueError:
                messagebox.showerror("Error", "La cantidad debe ser un numero valido")
        
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=15)
        
        ttk.Button(button_frame, text="Confirmar Retiro", command=confirmar_retiro).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancelar", command=retiro_window.destroy).pack(side=tk.RIGHT, padx=5)
        
        retiro_window.bind('<Return>', lambda event: confirmar_retiro())
    
    def agregar_producto(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Agregar Nuevo Producto")
        add_window.geometry("450x500")
        add_window.resizable(False, False)
        add_window.transient(self.root)
        add_window.grab_set()
        
        main_frame = ttk.Frame(add_window, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="NUEVO PRODUCTO", font=('Arial', 12, 'bold')).pack(pady=10)
        
        campos = [
            ("Nombre del Producto:", "entry_nombre"),
            ("Descripcion:", "entry_descripcion"),
            ("Categoria:", "entry_categoria"),
            ("Stock Inicial:", "entry_stock"),
            ("Stock Minimo (alerta):", "entry_stock_min"),
            ("Precio Unitario ($):", "entry_precio")
        ]
        
        entries = {}
        
        for label, key in campos:
            ttk.Label(main_frame, text=label).pack(pady=2)
            if "Descripcion" in label:
                entry = tk.Text(main_frame, width=40, height=3, font=('Arial', 9))
                entry.pack(pady=2)
            else:
                entry = ttk.Entry(main_frame, width=30, font=('Arial', 10))
                entry.pack(pady=2)
            entries[key] = entry
        
        def guardar_producto():
            try:
                nombre = entries['entry_nombre'].get().strip()
                descripcion = entries['entry_descripcion'].get("1.0", tk.END).strip() if hasattr(entries['entry_descripcion'], 'get') else entries['entry_descripcion'].get().strip()
                categoria = entries['entry_categoria'].get().strip()
                stock = int(entries['entry_stock'].get())
                stock_min = int(entries['entry_stock_min'].get())
                precio = float(entries['entry_precio'].get())
                
                if not nombre:
                    messagebox.showerror("Error", "El nombre del producto es obligatorio")
                    return
                
                if stock < 0 or stock_min < 0:
                    messagebox.showerror("Error", "Los valores de stock no pueden ser negativos")
                    return
                
                if precio < 0:
                    messagebox.showerror("Error", "El precio no puede ser negativo")
                    return
                
                query_check = "SELECT COUNT(*) FROM productos WHERE UPPER(nombre) = UPPER(:1)"
                cursor = self.db.execute_query(query_check, (nombre,))
                if cursor:
                    count = cursor.fetchone()[0]
                    if count > 0:
                        messagebox.showerror("Error", f"Ya existe un producto con el nombre: {nombre}")
                        return
                
                query = """
                INSERT INTO productos (id_producto, nombre, descripcion, categoria, stock_actual, stock_minimo, precio_unitario)
                VALUES (seq_productos.NEXTVAL, :1, :2, :3, :4, :5, :6)
                """
                self.db.execute_query(query, (nombre, descripcion, categoria, stock, stock_min, precio))
                
                messagebox.showinfo("Exito", "Producto agregado correctamente al inventario")
                add_window.destroy()
                self.actualizar_lista_productos()
                
            except ValueError:
                messagebox.showerror("Error", "Verifique que los valores numericos sean correctos")
            except Exception as e:
                messagebox.showerror("Error", f"Error al guardar: {str(e)}")
        
        ttk.Button(main_frame, text="Guardar Producto", command=guardar_producto).pack(pady=15)
        ttk.Button(main_frame, text="Cancelar", command=add_window.destroy).pack(pady=5)
    
    def verificar_alertas(self):
        productos = Producto.obtener_todos(self.db)
        
        productos_bajos = [p for p in productos if p.necesita_reabastecimiento() and p.stock_actual > 0]
        productos_agotados = [p for p in productos if p.stock_actual == 0]
        
        alertas = []
        
        if productos_agotados:
            alertas.append("PRODUCTOS AGOTADOS:\n")
            for producto in productos_agotados:
                alertas.append(f"   • {producto.nombre}\n")
        
        if productos_bajos:
            alertas.append("\nPRODUCTOS CON STOCK BAJO:\n")
            for producto in productos_bajos:
                alertas.append(f"   • {producto.nombre} - Stock: {producto.stock_actual} (Minimo: {producto.stock_minimo})\n")
        
        if alertas:
            mensaje = "".join(alertas)
            messagebox.showwarning("ALERTAS DE INVENTARIO", mensaje)
    
    def run(self):
        self.root.mainloop()